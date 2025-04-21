# File: routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.kyc import KYC
from models.user import User
from models.audit import AuditLog
from schemas.kyc import KYCUpload, KYCOut
from datetime import datetime
from typing import List
from utils.notifications import send_email  # NEW

router = APIRouter()

# === User submits KYC ===
@router.post("/submit", response_model=KYCOut)
def submit_kyc(
    payload: KYCUpload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != payload.user_id:
        raise HTTPException(status_code=403, detail="You can only submit your own KYC.")

    kyc = KYC(
        user_id=current_user.id,
        document_type=payload.document_type,
        document_url=payload.document_url,
        status="pending",
        submitted_at=datetime.utcnow()
    )
    db.add(kyc)
    db.commit()
    db.refresh(kyc)
    return kyc


# === User views their own KYC history ===
@router.get("/user", response_model=List[KYCOut])
def get_my_kyc(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(KYC).filter(KYC.user_id == current_user.id).order_by(KYC.submitted_at.desc()).all()


# === Admin views all pending KYCs ===
@router.get("/pending", response_model=List[KYCOut])
def get_pending_kyc(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")

    return db.query(KYC).filter(KYC.status == "pending").order_by(KYC.submitted_at.desc()).all()


# === Admin reviews (approve or reject) KYC ===
@router.put("/review/{kyc_id}", response_model=KYCOut)
def review_kyc(
    kyc_id: int,
    status: str,
    note: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'.")

    kyc = db.query(KYC).filter(KYC.id == kyc_id).first()
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC record not found")

    if kyc.status != "pending":
        raise HTTPException(status_code=409, detail="KYC already reviewed.")

    # Update KYC record
    kyc.status = status
    kyc.review_note = note
    kyc.reviewed_by = current_user.id
    db.commit()
    db.refresh(kyc)

    # Log audit action
    db.add(AuditLog(
        admin_id=current_user.id,
        action=f"KYC {status.upper()}",
        target_type="KYC",
        target_id=kyc.id
    ))
    db.commit()

    # Notify user via email
    user = db.query(User).filter(User.id == kyc.user_id).first()
    if user and user.email:
        send_email(
            to=user.email,
            subject=f"KYC {status.title()} Notification",
            body=(
                f"Hello {user.full_name or 'User'},\n\n"
                f"Your KYC submission has been {status.upper()}.\n"
                f"Note: {note or 'No remarks'}\n\n"
                f"Thank you,\nDealcross Team"
            )
        )

    return kyc
