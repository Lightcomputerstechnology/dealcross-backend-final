# File: schemas/deal.py

from pydantic import BaseModel
from typing import Optional

class DealBase(BaseModel):
    title: str
    amount: float
    status: Optional[str] = "pending"
    counterparty_email: str
    description: Optional[str] = None
    public_deal: bool = False

class DealOut(DealBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2+ support
