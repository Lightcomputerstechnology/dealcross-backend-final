# File: schemas/deal_schema.py

from pydantic import BaseModel

class DealCreate(BaseModel):
    title: str
    amount: float
    role: str
    escrow_type: str
    counterparty_email: str
