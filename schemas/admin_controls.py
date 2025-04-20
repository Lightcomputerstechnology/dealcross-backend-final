# File: schemas/admin_controls.py
from pydantic import BaseModel

class BlockAction(BaseModel):
    user_id: int
    reason: str | None = None

class DealApproval(BaseModel):
    deal_id: int
    note: str | None = None
