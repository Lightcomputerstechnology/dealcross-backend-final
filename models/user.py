from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base  # ✅ Correct Base import

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Updated relationship with foreign_keys
    user = relationship(
        "User",
        back_populates="wallet",
        foreign_keys=[user_id]  # ✅ Added explicitly
    )
    transactions = relationship("WalletTransaction", back_populates="wallet")
