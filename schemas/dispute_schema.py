# File: schemas/dispute_schema.py

from pydantic import BaseModel

class DisputeCreate(BaseModel):
    deal_id: int
    reason: str
    details: str
