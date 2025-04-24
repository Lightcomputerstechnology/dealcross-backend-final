from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class KYCUpload(BaseModel):
    user_id: int = Field(..., description="User ID submitting KYC document")
    document_type: str = Field(..., description="Type of KYC document (e.g., passport, ID card)")
    document_url: HttpUrl = Field(..., description="URL to the uploaded KYC document")

class KYCStatusUpdate(BaseModel):
    status: str = Field(..., description="New status for the KYC document", pattern="^(pending|approved|rejected)$")
    note: Optional[str] = Field(None, description="Optional note for approval/rejection")

class KYCOut(BaseModel):
    id: int
    user_id: int
    document_type: str
    document_url: HttpUrl
    status: str  # pending, approved, rejected
    review_note: Optional[str]
    submitted_at: datetime

    model_config = {"from_attributes": True}