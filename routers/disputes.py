# File: routers/disputes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from core.dependencies import require_admin  # ✅ Replaces manual admin check
from models.dispute import Dispute, DisputeStatus
from models.deal import Deal
from schemas.dispute_schema import DisputeCreate, DisputeOut
from typing import List
from datetime import datetime

router = APIRouter()

# === User submits dispute ===
@router.post("/submit", response_model=DisputeOut)
def submit_dispute(
    payload: DisputeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deal = db.query(Deal).filter(Deal.id == payload.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Only creator or counterparty can dispute
    if current_user.id not in [deal.creator_id, deal.counterparty_id]:
        raise HTTPException(status_code=403, detail="Access denied")

    dispute = Dispute(
        deal_id=payload.deal_id,
        user_id=current_user.id,  # ✅ Replaces submitted_by
        reason=payload.reason,
        details=payload.details
    )

    db.add(dispute)
    db.commit()
    db.refresh(dispute)

    return dispute

# === User views their disputes ===
@router.get("/my-disputes", response_model=List[DisputeOut])
def get_my_disputes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    disputes = db.query(Dispute).filter(Dispute.user_id == current_user.id).order_by(Dispute.created_at.desc()).all()
    return disputes

# === Admin views all disputes ===
@router.get("/logs", response_model=List[DisputeOut])
def get_disputes(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Dispute).order_by(Dispute.created_at.desc()).all()

# === Admin resolves dispute ===
@router.put("/resolve/{dispute_id}", response_model=DisputeOut)
def resolve_dispute(
    dispute_id: int,
    resolution: str,  # 'resolved' or 'rejected'
    note: str = "",
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    if dispute.status != DisputeStatus.open:
        raise HTTPException(status_code=409, detail="Dispute already handled")

    if resolution not in ["resolved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid resolution option")

    dispute.status = resolution
    dispute.resolution_note = note
    dispute.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(dispute)
    return dispute
