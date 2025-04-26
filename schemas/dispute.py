# File: src/schemas/dispute.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DisputeCreate(BaseModel):
    deal_id: int = Field(..., description="ID of the deal to dispute")
    reason: str = Field(..., description="Reason for disputing")
    details: Optional[str] = Field(None, description="Additional details")

class DisputeResolve(BaseModel):
    dispute_id: int = Field(..., description="ID of the dispute to resolve")
    resolution: str = Field(..., description="Resolution summary")
    note: Optional[str] = Field(None, description="Optional note")

class DisputeOut(BaseModel):
    id: int
    deal_id: int
    status: str
    reason: str
    details: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}