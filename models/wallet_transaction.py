# File: models/wallet_transaction.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from core.database import Base

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # e.g., 'fund', 'deduct', 'transfer'
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
