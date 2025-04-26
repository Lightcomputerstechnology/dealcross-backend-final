from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    __table_args__ = {'extend_existing': True}  # ✅ Prevents duplicate table issues

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="pending")  # e.g., pending, resolved
    reported_by = Column(Integer, ForeignKey("users.id"))  # Links to user who reported
    reported_at = Column(DateTime, default=datetime.utcnow)

    # Relationship (matches user.py)
    reporter = relationship("User", back_populates="fraud_alerts")