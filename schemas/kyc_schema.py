from pydantic import BaseModel
from typing import Optional


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
    submitted_at: str  # ISO format

    model_config = {"from_attributes": True}
