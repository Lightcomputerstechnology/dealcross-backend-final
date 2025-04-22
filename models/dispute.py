# File: models/dispute.py

from core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
import enum

class DisputeStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"
    rejected = "rejected"

class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ Replaces submitted_by
    reason = Column(String, nullable=False)
    details = Column(String, nullable=True)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.open)  # ✅ Status flow
    resolution_note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
