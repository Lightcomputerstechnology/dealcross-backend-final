# File: schemas/deal.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

# ─────────── ENUMS ───────────

class DealStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    disputed = "disputed"
    cancelled = "cancelled"
    paired = "paired"

# ─────────── BASE SCHEMA ───────────

class DealBase(BaseModel):
    title: str
    amount: float
    description: Optional[str] = None
    public_deal: bool = False  # renamed for clarity in code

# ─────────── CREATE ───────────

class DealCreate(DealBase):
    counterparty_id: Optional[int] = None  # may be null initially for public deals

# ─────────── RESPONSE (USER VIEW) ───────────

class DealOut(DealBase):
    id: int
    creator_id: int
    counterparty_id: Optional[int]
    status: DealStatus
    is_flagged: Optional[bool] = False
    pairing_confirmed: Optional[bool] = False
    created_at: datetime

    model_config = {"from_attributes": True}

# ─────────── RESPONSE (PAIRING QUEUE) ───────────

class PairingOut(BaseModel):
    id: int
    creator_id: int
    title: str
    amount: float
    public_deal: bool
    status: DealStatus

    model_config = {"from_attributes": True}

# ─────────── ADMIN ACTION ───────────

class DealAdminUpdate(BaseModel):
    status: Optional[DealStatus] = None
    approval_note: Optional[str] = None
    is_flagged: Optional[bool] = None