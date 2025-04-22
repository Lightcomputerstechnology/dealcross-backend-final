from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class DisputeStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"
    rejected = "rejected"

class DisputeCreate(BaseModel):
    deal_id: int
    reason: str
    details: Optional[str] = None

    model_config = {"from_attributes": True}

class DisputeOut(BaseModel):
    id: int
    deal_id: int
    user_id: int  # ✅ Replaces submitted_by
    reason: str
    details: Optional[str]
    status: DisputeStatus  # ✅ Adds status tracking
    resolution_note: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}
