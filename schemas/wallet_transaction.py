# File: schemas/wallet_transaction.py

from pydantic import BaseModel
from datetime import datetime

class WalletTransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    description: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
