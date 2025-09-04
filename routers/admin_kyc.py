# File: routers/admin_kyc.py

from typing import Dict, Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import get_current_user  # Supabase-aware claims
from core.supabase_client import get_profile_is_admin  # server-side admin check

from models.kyc import KYCRequest, KYCStatus
from models.user import User
from schemas.kyc_schema import KYCStatusUpdate, KYCOut

router = APIRouter(prefix="/admin/kyc", tags=["KYC Admin"])

# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user

# ─────────── ADMIN ACCESS VALIDATION (Supabase profiles.is_admin or local) ───────────
async def require_admin(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    supa_user_id = claims.get("sub")
    is_admin = False
    if supa_user_id:
        flag = get_profile_is_admin(supa_user_id)
        is_admin = bool(flag)

    if not is_admin and (getattr(db_user, "is_admin", False) or getattr(db_user, "role", "") == "admin"):
        is_admin = True

    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")
    return db_user

# ─────────── LIST PENDING REQUESTS ───────────
@router.get("/pending", response_model=List[KYCOut], summary="List all pending KYC requests")
async def list_pending_kyc(_: User = Depends(require_admin)):
    pending = await KYCRequest.filter(status=KYCStatus.pending).order_by("submitted_at")
    return [await KYCOut.from_tortoise_orm(k) for k in pending]

# ─────────── APPROVE OR REJECT A REQUEST ───────────
@router.post("/{kyc_id}/review", response_model=KYCOut, summary="Approve or reject a KYC request")
async def review_kyc(
    kyc_id: int,
    update: KYCStatusUpdate,
    _: User = Depends(require_admin),
):
    kyc = await KYCRequest.get_or_none(id=kyc_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="KYC request not found.")
    if kyc.status != KYCStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending requests can be reviewed.")

    kyc.status = update.status
    kyc.review_note = update.note
    await kyc.save()

    return await KYCOut.from_tortoise_orm(kyc)
