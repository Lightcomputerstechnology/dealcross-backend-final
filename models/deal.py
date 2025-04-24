from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
import enum
from datetime import datetime

class DealStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    disputed = "disputed"
    cancelled = "cancelled"

class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(DealStatus), default=DealStatus.pending)
    description = Column(String, nullable=True)
    public_deal = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)  # Fraud flag
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    counterparty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_deals")
    counterparty = relationship("User", foreign_keys=[counterparty_id], back_populates="counterparty_deals")