from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from core.database import Base

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)  # ✅ Correct ForeignKey
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # e.g., 'fund', 'deduct', 'transfer'
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Wallet
    wallet = relationship("Wallet", back_populates="transactions")  # ✅ Added this
