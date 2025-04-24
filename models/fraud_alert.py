from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to user
    alert_type = Column(String, nullable=False)  # Example: 'suspicious_activity', 'dispute_flag', etc.
    description = Column(Text, nullable=True)  # Details of the alert
    status = Column(String, default="unresolved")  # 'unresolved', 'resolved'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to User
    user = relationship("User", back_populates="fraud_alerts")
