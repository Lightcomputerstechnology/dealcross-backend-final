# File: routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.kyc import KYC
from models.user import User
from schemas.kyc import KYCUpload, KYCOut
from typing import List
from datetime import datetime

router = APIRouter()

# === User uploads KYC document ===
@router.post("/submit", response_model=KYCOut)
def submit_kyc(payload: KYCUpload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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


# === Admin fetches all pending KYC ===
@router.get("/pending", response_model=List[KYCOut])
def get_pending_kyc(db: Session = Depends(get_db)):
    return db.query(KYC).filter(KYC.status == "pending").order_by(KYC.submitted_at.desc()).all()


# === Admin approves or rejects KYC ===
@router.put("/review/{kyc_id}", response_model=KYCOut)
def review_kyc(kyc_id: int, status: str, note: str = "", db: Session = Depends(get_db)):
    kyc = db.query(KYC).filter(KYC.id == kyc_id).first()
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC record not found")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

    kyc.status = status
    kyc.review_note = note
    db.commit()
    db.refresh(kyc)
    return kyc


# === User fetches their KYC status ===
@router.get("/user/{user_id}", response_model=List[KYCOut])
def get_user_kyc(user_id: int, db: Session = Depends(get_db)):
    return db.query(KYC).filter(KYC.user_id == user_id).order_by(KYC.submitted_at.desc()).all()
