# File: src/routers/disputes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user

from models.dispute import Dispute, DisputeStatus
from models.user import User
from models.fraud_alert import FraudAlert

from schemas.dispute import DisputeCreate, DisputeOut, DisputeResolve
from schemas.fraud_alert import FraudAlertOut

# Notification helpers
from utils.notifications import create_notification, send_email_notification

router = APIRouter(prefix="/disputes", tags=["Disputes"])


@router.post("/submit", response_model=DisputeOut, summary="Submit a new dispute")
def submit_dispute(
    payload: DisputeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DisputeOut:
    """
    Create a new dispute record.
    """
    new_dispute = Dispute(
        deal_id=payload.deal_id,
        user_id=current_user.id,
        reason=payload.reason,
        details=payload.details,
        status=DisputeStatus.pending,
    )
    db.add(new_dispute)
    db.commit()
    db.refresh(new_dispute)

    # Example: notify admin of new dispute
    admin_alert = FraudAlert(
        user_id=current_user.id,
        alert_type="dispute_submitted",
        description=f"User {current_user.id} submitted dispute {new_dispute.id}"
    )
    db.add(admin_alert)
    db.commit()

    return new_dispute


@router.get("/logs", response_model=list[DisputeOut], summary="Admin: View all disputes")
def view_dispute_logs(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user),
) -> list[DisputeOut]:
    if admin.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return (
        db.query(Dispute)
          .order_by(Dispute.created_at.desc())
          .all()
    )


@router.post("/{dispute_id}/resolve", response_model=DisputeOut, summary="Admin: Resolve a dispute")
def resolve_dispute(
    dispute_id: int,
    payload: DisputeResolve,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user),
) -> DisputeOut:
    if admin.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found.")

    dispute.status = payload.status
    db.commit()
    db.refresh(dispute)

    # Notify the user who raised the dispute
    send_email_notification(
        background_tasks=Depends(),  # ensure you inject BackgroundTasks in your actual endpoint
        to_email=dispute.user.email,
        subject="Your dispute has been resolved",
        body=f"Hello {dispute.user.full_name or 'User'}, your dispute #{dispute.id} is now {dispute.status}."
    )
    create_notification(
        db=db,
        user_id=dispute.user_id,
        title="Dispute Resolved",
        message=f"Your dispute #{dispute.id} has been marked {dispute.status}."
    )

    return dispute