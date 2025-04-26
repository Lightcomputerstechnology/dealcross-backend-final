# File: src/routers/disputes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.dispute import Dispute, DisputeStatus
from schemas.dispute import DisputeCreate, DisputeResolve, DisputeOut
from schemas.fraud_alert import FraudAlertCreate, FraudAlertOut
from models.fraud_alert import FraudAlert
from models.deal import Deal, DealStatus
from models.fee_transaction import FeeTransaction
from models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter(prefix="/disputes", tags=["Disputes"])

@router.post("/", response_model=DisputeOut, summary="Submit a dispute")
def create_dispute(
    dispute: DisputeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new = Dispute(
        deal_id=dispute.deal_id,
        user_id=current_user.id,
        reason=dispute.reason,
        details=dispute.details,
        status=DisputeStatus.open
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.put("/{dispute_id}/resolve", response_model=DisputeOut, summary="Resolve a dispute")
def resolve_dispute(
    dispute_id: int,
    resolution: DisputeResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not d or d.status != DisputeStatus.open:
        raise HTTPException(status_code=400, detail="Cannot resolve this dispute.")
    d.status = DisputeStatus.resolved
    d.resolution = resolution.resolution
    d.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(d)
    return d

# … any other dispute/fraud‐alert endpoints …