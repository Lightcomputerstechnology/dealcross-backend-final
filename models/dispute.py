from core.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum as SAEnum,
    DateTime,
)
from sqlalchemy.orm import relationship
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(String, nullable=False)
    details = Column(String, nullable=True)
    status = Column(SAEnum(DisputeStatus), default=DisputeStatus.open)
    resolution_note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # ← Add this:
    fraud_alerts = relationship(
        "FraudAlert",
        back_populates="dispute",
        foreign_keys="FraudAlert.dispute_id",
        cascade="all, delete-orphan",
    )