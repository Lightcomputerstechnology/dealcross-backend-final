from pydantic import BaseModel
from typing import Optional


class DealCreate(BaseModel):
    buyer_id: int
    seller_id: int
    title: str
    amount: float
    currency: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class DealOut(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    title: str
    amount: float
    currency: str
    description: Optional[str] = None
    is_funded: bool
    is_delivered: bool
    is_released: bool
    is_disputed: bool

    model_config = {"from_attributes": True}
