# File: routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.kyc import KYC
from models.user import User
from models.audit import AuditLog  # if logging admin decisions
from schemas.kyc import KYCUpload, KYCOut
from typing import List
from datetime import datetime

router = APIRouter()

# === User submits KYC (auth enforced) ===
@router.post("/submit", response_model=KYCOut)
def submit_kyc(
    payload: KYCUpload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != payload.user_id:
        raise HTTPException(status_code=403, detail="You can only submit your own KYC.")

    kyc = KYC(
        user_id=payload.user_id,
        document_type=payload.document_type,
        document_url=payload.document_url,
        status="pending",
        submitted_at=datetime.utcnow()
    )
    db.add(kyc)
    db.commit()
    db.refresh(kyc)
    return kyc


# === Admin views all pending KYC ===
@router.get("/pending", response_model=List[KYCOut])
def get_pending_kyc(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")
    
    return db.query(KYC).filter(KYC.status == "pending").order_by(KYC.submitted_at.desc()).all()


# === Admin approves or rejects ===
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
    
    kyc = db.query(KYC).filter(KYC.id == kyc_id).first()
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC record not found")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

    kyc.status = status
    kyc.review_note = note
    kyc.reviewed_by = current_user.id  # optional field
    db.commit()
    db.refresh(kyc)

    # Optional: log admin decision
    log = AuditLog(
        admin_id=current_user.id,
        action=f"KYC {status.upper()}",
        target_type="KYC",
        target_id=kyc_id,
    )
    db.add(log)
    db.commit()

    # Placeholder: send user notification (email, SMS, etc.)
    # notify_user(kyc.user_id, f"KYC status updated: {status}")

    return kyc


# === User views own KYC status ===
@router.get("/user", response_model=List[KYCOut])
def get_my_kyc(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(KYC).filter(KYC.user_id == current_user.id).order_by(KYC.submitted_at.desc()).all()
