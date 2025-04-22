# File: schemas/wallet.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WalletCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user who owns this wallet")
    balance: float = Field(0.0, ge=0.0, description="Initial balance of the wallet, must be non-negative")

class WalletUpdate(BaseModel):
    balance: float = Field(..., ge=0.0, description="Updated balance after transaction, must be non-negative")

class WalletOut(BaseModel):
    id: int = Field(..., description="Unique identifier for the wallet")
    user_id: int = Field(..., description="ID of the user who owns this wallet")
    balance: float = Field(..., description="Current balance in the wallet")
    created_at: datetime = Field(..., description="Timestamp when the wallet was created")

    class Config:
        from_attributes = True  # For Pydantic v2 (replaces orm_mode)
