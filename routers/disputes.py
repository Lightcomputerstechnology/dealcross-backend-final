# File: routers/disputes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.dispute import Dispute
from models.user import User
from models.deal import Deal
from schemas.dispute_schema import DisputeCreate
from core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit")
def submit_dispute(payload: DisputeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(Deal).filter(Deal.id == payload.deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    dispute = Dispute(
        deal_id=payload.deal_id,
        reason=payload.reason,
        details=payload.details,
        submitted_by=current_user.email
    )

    db.add(dispute)
    db.commit()
    db.refresh(dispute)

    return {"message": "Dispute submitted", "dispute_id": dispute.id}

@router.get("/logs")
def get_disputes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    disputes = db.query(Dispute).all()
    return [
        {
            "deal_id": d.deal_id,
            "reason": d.reason,
            "submitted_by": d.submitted_by,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for d in disputes
    ]
