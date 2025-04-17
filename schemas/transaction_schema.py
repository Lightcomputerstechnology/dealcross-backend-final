from pydantic import BaseModel
from typing import Literal


class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    type: Literal["credit", "debit"]
    reference: str

    model_config = {"from_attributes": True}


class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    type: str
    reference: str
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
