from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from core.database import Base

class FeeTransaction(Base):
    __tablename__ = 'fee_transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # 'funding', 'escrow', 'share_buy', 'share_sell'
    amount = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="fee_transactions")
