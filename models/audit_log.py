# File: models/audit_log.py

from sqlalchemy import Column, Integer, String, DateTime, Table
from sqlalchemy.orm import declarative_base
from core.database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}  # Add this line

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    performed_by = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=True)