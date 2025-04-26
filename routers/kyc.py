# File: src/routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from core.database   import get_db
from core.security   import get_current_user
from models.kyc      import KYC
from models.user     import User
from models.audit_log import AuditLog
from schemas.kyc     import KYCUpload, KYCOut
from utils.notifications import send_email

router = APIRouter(prefix="/kyc", tags=["KYC Verification"])

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
MAX_FILE_SIZE       = 5 * 1024 * 1024  # 5MB

def validate_kyc_file(file: UploadFile):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type .{ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

@router.post("/upload-file", summary="Upload KYC file")
async def upload_kyc_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    validate_kyc_file(file)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Max size is {MAX_FILE_SIZE//(1024*1024)}MB.")
    # TODO: replace with real storage/upload logic
    url = f"https://mock-storage/dealcross/kyc/{file.filename}"
    return {"message": "File uploaded", "document_url": url}

@router.post("/submit", response_model=KYCOut, summary="Submit KYC for review")
def submit_kyc(payload: KYCUpload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.user_id != current_user.id:
        raise HTTPException(403, "Can only submit your own KYC.")
    kyc = KYC(
        user_id       = current_user.id,
        document_type = payload.document_type,
        document_url  = payload.document_url,
        status        = "pending",
        submitted_at  = datetime.utcnow()
    )
    db.add(kyc)
    db.commit()
    db.refresh(kyc)
    return kyc

@router.get("/user", response_model=List[KYCOut], summary="Your KYC submissions")
def get_my_kyc(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(KYC)
          .filter(KYC.user_id == current_user.id)
          .order_by(KYC.submitted_at.desc())
          .all()
    )

@router.get("/pending", response_model=List[KYCOut], summary="Admin: View all pending KYCs")
def get_pending_kyc(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access only.")
    return (
        db.query(KYC)
          .filter(KYC.status == "pending")
          .order_by(KYC.submitted_at.desc())
          .all()
    )

@router.put("/review/{kyc_id}", response_model=KYCOut, summary="Admin: Approve/Reject KYC")
def review_kyc(
    kyc_id: int,
    status: str,
    note: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access only.")
    if status not in ("approved", "rejected"):
        raise HTTPException(400, "Status must be 'approved' or 'rejected'.")

    kyc = db.query(KYC).get(kyc_id)
    if not kyc:
        raise HTTPException(404, "KYC not found.")
    if kyc.status != "pending":
        raise HTTPException(409, "KYC already reviewed.")

    kyc.status        = status
    kyc.review_note   = note
    kyc.reviewed_by   = current_user.id
    kyc.reviewed_at   = datetime.utcnow()
    db.add(AuditLog(
        admin_id   = current_user.id,
        action     = f"KYC {status.upper()}",
        target_type= "KYC",
        target_id  = kyc.id
    ))
    db.commit()
    db.refresh(kyc)

    # send email
    user = db.query(User).get(kyc.user_id)
    if user and user.email:
        send_email(
            to      = user.email,
            subject = f"KYC {status.title()} Notification",
            body    = (
                f"Hello {user.full_name or 'User'},\n\n"
                f"Your KYC has been {status.upper()}.\nNote: {note or 'No remarks'}"
            )
        )

    return kyc