from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base  # ✅ Correct Base import

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)  # ✅ Unique for one wallet per user
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")  # ✅ You can change currency default if needed
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="wallet")  # ✅ Back to User model
    transactions = relationship("WalletTransaction", back_populates="wallet")  # ✅ For WalletTransaction model
