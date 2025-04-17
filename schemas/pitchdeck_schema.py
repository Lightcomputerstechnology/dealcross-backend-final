from pydantic import BaseModel
from typing import Optional


class PitchDeckUpload(BaseModel):
    investor_id: int
    title: str
    file_url: str
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class PitchDeckOut(BaseModel):
    id: int
    investor_id: int
    title: str
    file_url: str
    notes: Optional[str]
    uploaded_at: str  # ISO format

    model_config = {"from_attributes": True}
