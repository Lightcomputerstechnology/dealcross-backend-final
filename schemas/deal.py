from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class DealStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    disputed = "disputed"
    cancelled = "cancelled"

class DealBase(BaseModel):
    title: str
    amount: float
    description: Optional[str] = None
    public_deal: bool = False

class DealCreate(DealBase):
    counterparty_id: int

class DealOut(DealBase):
    id: int
    creator_id: int
    counterparty_id: int
    status: DealStatus
    created_at: datetime
    is_flagged: bool

    model_config = {"from_attributes": True}

class DealAdminUpdate(BaseModel):
    status: Optional[DealStatus] = None
    approval_note: Optional[str] = None
    is_flagged: Optional[bool] = None