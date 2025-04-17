from pydantic import BaseModel
from typing import Optional


class ReportCreate(BaseModel):
    title: str
    content: str
    submitted_by: str

    model_config = {"from_attributes": True}


class ReportOut(BaseModel):
    id: int
    title: str
    content: str
    submitted_by: str
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
