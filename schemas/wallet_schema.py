from pydantic import BaseModel
from typing import Literal


class WalletCreate(BaseModel):
    user_id: int
    currency: Literal["NGN", "USD", "BTC", "USDT"]
    balance: float = 0.0

    model_config = {"from_attributes": True}


class WalletOut(BaseModel):
    id: int
    user_id: int
    currency: str
    balance: float

    model_config = {"from_attributes": True}
