from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

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
    is_flagged = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    counterparty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fee_applied = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_deals")
    counterparty = relationship("User", foreign_keys=[counterparty_id], back_populates="counterparty_deals")