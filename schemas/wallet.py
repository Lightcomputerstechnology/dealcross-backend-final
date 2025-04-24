from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class WalletOut(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str
    updated_at: datetime

    model_config = {"from_attributes": True}

class TransactionOut(BaseModel):
    id: int
    amount: float
    transaction_type: str
    description: Optional[str]
    timestamp: datetime

    model_config = {"from_attributes": True}

class FundWallet(BaseModel):
    amount: float = Field(..., gt=0.0, description="Amount to fund the wallet.")