from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class KYCUpload(BaseModel):
    user_id: int
    document_type: str  # e.g., "passport", "ID card"
    document_url: str
    status: Optional[str] = "pending"

    model_config = {"from_attributes": True}


class KYCOut(BaseModel):
    id: int
    user_id: int
    document_type: str
    document_url: str
    status: str
    submitted_at: datetime
    review_note: Optional[str] = None

    model_config = {"from_attributes": True}


class KYCUpdate(BaseModel):
    status: str  # e.g., "approved", "rejected"
    review_note: Optional[str] = None
