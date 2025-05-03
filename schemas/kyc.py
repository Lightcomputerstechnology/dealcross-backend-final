# File: schemas/kyc_schema.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from models.kyc import KYCStatus  # Enum for status values

# ─────────── SUBMIT KYC PAYLOAD ───────────
class KYCRequestCreate(BaseModel):
    document_type: str = Field(..., description="Type of KYC document (e.g., passport, ID card)")
    document_url: HttpUrl = Field(..., description="URL of the uploaded document")

# ─────────── ADMIN STATUS UPDATE ───────────
class KYCStatusUpdate(BaseModel):
    status: KYCStatus = Field(..., description="New status: pending, approved, or rejected")
    note: Optional[str] = Field(None, description="Optional note for admin review")

# ─────────── KYC RESPONSE SCHEMA ───────────
class KYCRequestOut(BaseModel):
    id: int
    user_id: int
    document_type: str
    document_url: HttpUrl
    status: KYCStatus
    review_note: Optional[str] = None
    submitted_at: datetime

    model_config = {"from_attributes": True}