from sqlalchemy import Column, Integer, String, Enum, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

# Enum for Fee Types
class FeeType(str, enum.Enum):
    funding = "funding"
    escrow = "escrow"
    share_buy = "share_buy"
    share_sell = "share_sell"

class FeeTransaction(Base):
    __tablename__ = "fee_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship("User", back_populates="fee_transactions")