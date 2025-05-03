from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class KYCStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class KYCRequestCreate(BaseModel):
    document_type: str
    document_url: str


class KYCRequestOut(BaseModel):
    id: int
    document_type: str
    document_url: str
    status: str
    submitted_at: datetime

    class Config:
        from_attributes = True


class KYCStatusUpdate(BaseModel):
    status: KYCStatus

    model_config = {"from_attributes": True}