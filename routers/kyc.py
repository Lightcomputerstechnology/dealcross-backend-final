# File: routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException
from models.kyc import KYCRequest, KYCStatus
from core.security import get_current_user
from tortoise.exceptions import DoesNotExist
from schemas.kyc_schema import KYCRequestCreate, KYCRequestOut
from typing import List
from datetime import datetime

router = APIRouter()

# Submit new KYC request
@router.post("/", response_model=KYCRequestOut)
async def submit_kyc(kyc_data: KYCRequestCreate, current_user=Depends(get_current_user)):
    kyc = await KYCRequest.create(
        user=current_user,
        document_type=kyc_data.document_type,
        document_url=kyc_data.document_url,
        status=KYCStatus.pending,
        submitted_at=datetime.utcnow()
    )
    return kyc

# View my KYC status
@router.get("/my-kyc", response_model=List[KYCRequestOut])
async def view_my_kyc(current_user=Depends(get_current_user)):
    return await KYCRequest.filter(user=current_user).order_by("-submitted_at")
