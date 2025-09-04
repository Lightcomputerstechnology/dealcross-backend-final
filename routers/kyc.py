# File: routers/kyc.py

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from core.security import get_current_user
from models.kyc import KYCRequest, KYCStatus
from schemas.kyc_schema import KYCRequestCreate, KYCRequestOut
from models.user import User

router = APIRouter(prefix="/kyc", tags=["KYC Verification"])


# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


# ─────────── SUBMIT KYC ───────────
@router.post("/", response_model=KYCRequestOut, summary="Submit new KYC request")
async def submit_kyc(
    kyc_data: KYCRequestCreate,
    current_user: User = Depends(resolve_db_user)
):
    existing = await KYCRequest.filter(user=current_user, status=KYCStatus.pending).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have a pending KYC request.")

    kyc = await KYCRequest.create(
        user=current_user,
        document_type=kyc_data.document_type,
        document_url=kyc_data.document_url,
        status=KYCStatus.pending,
        submitted_at=datetime.utcnow()
    )
    return await KYCRequestOut.from_tortoise_orm(kyc)

# ─────────── VIEW MY KYC STATUS ───────────
@router.get("/my-kyc", response_model=List[KYCRequestOut], summary="View your submitted KYC history")
async def view_my_kyc(current_user: User = Depends(resolve_db_user)):
    kyc_list = await KYCRequest.filter(user=current_user).order_by("-submitted_at")
    return [await KYCRequestOut.from_tortoise_orm(k) for k in kyc_list]
