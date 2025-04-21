# File: schemas/deal.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# === Base Deal Schema ===
class DealBase(BaseModel):
    title: str
    amount: float
    status: Optional[str] = "pending"
    counterparty_email: Optional[str]
    description: Optional[str] = None
    public_deal: Optional[bool] = False
    escrow_type: Optional[str] = "default"
    role: Optional[str] = "buyer"

# === Output Deal Schema for APIs ===
class DealOut(DealBase):
    id: int
    creator_id: Optional[int]
    counterparty_id: Optional[int]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# === Deal Creation Payload ===
class DealCreate(DealBase):
    pass
