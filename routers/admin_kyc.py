# File: routers/admin_kyc.py

from fastapi import APIRouter, Depends, HTTPException, status
from models.kyc import KYCRequest, KYCStatus
from models.user import User
from core.security import get_current_user
from schemas.kyc_schema import KYCStatusUpdate, KYCOut
from typing import List

router = APIRouter(prefix="/admin/kyc", tags=["KYC Admin"])

# ─────────── ADMIN ACCESS VALIDATION ───────────
def require_admin(user: User):
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only.")
    return user

# ─────────── LIST PENDING REQUESTS ───────────
@router.get("/pending", response_model=List[KYCOut], summary="List all pending KYC requests")
async def list_pending_kyc(current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    pending = await KYCRequest.filter(status=KYCStatus.pending).order_by("submitted_at")
    return [await KYCOut.from_tortoise_orm(k) for k in pending]

# ─────────── APPROVE OR REJECT A REQUEST ───────────
@router.post("/{kyc_id}/review", response_model=KYCOut, summary="Approve or reject a KYC request")
async def review_kyc(
    kyc_id: int,
    update: KYCStatusUpdate,
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    kyc = await KYCRequest.get_or_none(id=kyc_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC request not found.")
    if kyc.status != KYCStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending requests can be reviewed.")

    kyc.status = update.status
    kyc.review_note = update.note
    await kyc.save()

    return await KYCOut.from_tortoise_orm(kyc)