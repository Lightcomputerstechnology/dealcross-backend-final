# File: src/schemas/dispute.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from models.dispute import DisputeStatus


class DisputeBase(BaseModel):
    deal_id: int = Field(..., description="ID of the deal being disputed")
    reason: str = Field(..., description="Brief reason for the dispute")
    details: Optional[str] = Field(None, description="Optional additional details")


class DisputeCreate(DisputeBase):
    """Payload for submitting a new dispute."""


class DisputeOut(DisputeBase):
    """What we return when looking up disputes."""
    id: int
    user_id: int
    status: DisputeStatus
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class DisputeResolve(BaseModel):
    """Payload for an admin resolving a dispute."""
    status: DisputeStatus