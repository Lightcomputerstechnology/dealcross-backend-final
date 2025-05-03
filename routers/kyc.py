# File: routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException
from models.kyc import KYCRequest, KYCStatus
from core.security import get_current_user
from schemas.kyc_schema import KYCRequestCreate, KYCRequestOut
from typing import List
from datetime import datetime
from models.user import User

router = APIRouter(prefix="/kyc", tags=["KYC Verification"])

# ─────────── SUBMIT KYC ───────────
@router.post("/", response_model=KYCRequestOut, summary="Submit new KYC request")
async def submit_kyc(
    kyc_data: KYCRequestCreate,
    current_user: User = Depends(get_current_user)
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
async def view_my_kyc(current_user: User = Depends(get_current_user)):
    kyc_list = await KYCRequest.filter(user=current_user).order_by("-submitted_at")
    return [await KYCRequestOut.from_tortoise_orm(k) for k in kyc_list]