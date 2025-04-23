# File: models/audit_log.py

from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)  # e.g., 'User Login', 'Deal Created'
    performed_by = Column(String, nullable=False)  # Username or user ID
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=True)  # Optional: additional details
