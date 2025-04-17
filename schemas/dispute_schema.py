from pydantic import BaseModel
from typing import Optional


class DisputeCreate(BaseModel):
    deal_id: int
    reason: str
    details: Optional[str] = None

    model_config = {"from_attributes": True}


class DisputeOut(BaseModel):
    id: int
    deal_id: int
    reason: str
    details: Optional[str]
    submitted_by: str
    created_at: str  # ISO date format

    model_config = {"from_attributes": True}
