# File: schemas/deal.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# === Shared Deal Structure ===
class DealBase(BaseModel):
    title: str
    amount: float
    status: str
    counterparty_email: EmailStr
    description: Optional[str] = None
    public_deal: bool = False


# === For Creating New Deals ===
class DealCreate(DealBase):
    escrow_type: Optional[str] = "standard"
    role: Optional[str] = "buyer"


# === For Returning Deal Data (User/Admin Use) ===
class DealOut(DealBase):
    id: int
    creator_id: Optional[int]
    counterparty_id: Optional[int]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# === For Admin to Update Deal Status ===
class DealAdminUpdate(BaseModel):
    status: Optional[str] = None
    approval_note: Optional[str] = None
    is_flagged: Optional[bool] = None
