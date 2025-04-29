# File: schemas/kyc_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
