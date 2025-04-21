# File: models/audit.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
