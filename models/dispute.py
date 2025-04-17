# File: models/dispute.py

from core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

class Dispute(Base):
    __tablename__ = "disputes"
    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    reason = Column(String)
    details = Column(String)
    submitted_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
