from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from core.database import Base
import enum

# ✅ Define FeeType Enum
class FeeType(str, enum.Enum):
    funding = "funding"
    escrow = "escrow"
    share_buy = "share_buy"
    share_sell = "share_sell"

class FeeTransaction(Base):
    __tablename__ = 'fee_transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(SQLAlchemyEnum(FeeType), nullable=False)  # ✅ Use Enum for type
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="fee_transactions")
