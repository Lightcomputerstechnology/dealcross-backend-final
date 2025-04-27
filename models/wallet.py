from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship(
        "User",
        back_populates="wallet",
        foreign_keys=[user_id]  # ✅ Explicitly set foreign key
    )
    transactions = relationship("WalletTransaction", back_populates="wallet", cascade="all, delete")
