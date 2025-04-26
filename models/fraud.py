from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="unresolved")
    created_at = Column(DateTime, default=datetime.utcnow)

    # ← New FK to Dispute
    dispute_id = Column(Integer, ForeignKey("disputes.id"), nullable=True)

    # ← back-populate the Dispute link
    dispute = relationship(
        "Dispute",
        back_populates="fraud_alerts",
        foreign_keys=[dispute_id]
    )

    # ← your existing user link
    user = relationship("User", back_populates="fraud_alerts", foreign_keys=[user_id])