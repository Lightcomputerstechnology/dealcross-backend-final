# File: models/wallet.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(Float, default=1.0)  # e.g., 1 for USD, or replace with Enum later
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
