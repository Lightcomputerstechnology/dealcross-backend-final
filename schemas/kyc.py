# File: schemas/kyc.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class KYCUpload(BaseModel):
    user_id: int = Field(..., description="User ID submitting KYC document")
    document_type: str = Field(..., description="Type of KYC document (e.g., passport, ID card)")
    document_url: HttpUrl = Field(..., description="URL to the uploaded KYC document")

class KYCStatusUpdate(BaseModel):
    status: str = Field(..., description="New status for the KYC document", pattern="^(pending|approved|rejected)$")

class KYCOut(BaseModel):
    id: int = Field(..., description="KYC record ID")
    user_id: int = Field(..., description="User ID")
    document_type: str = Field(..., description="Type of KYC document")
    document_url: HttpUrl = Field(..., description="Document URL")
    status: str = Field(..., description="Current KYC status")
    submitted_at: datetime = Field(..., description="Timestamp when the KYC was submitted")

    model_config = {
        "from_attributes": True  # Pydantic v2 compatibility
    }
