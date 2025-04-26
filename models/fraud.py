from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    __table_args__ = {'extend_existing': True}  # Avoids conflict if table exists

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who the alert is about
    alert_type = Column(String, nullable=False)  # e.g., 'suspicious_activity', 'dispute_flag'
    description = Column(Text, nullable=True)  # Detailed description
    status = Column(String, default="unresolved")  # 'unresolved', 'resolved'
    created_at = Column(DateTime, default=datetime.utcnow)

    reported_by = Column(Integer, ForeignKey("users.id"))  # Who reported (could be admin or system)
    reported_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="fraud_alerts")
    reporter = relationship("User", foreign_keys=[reported_by])