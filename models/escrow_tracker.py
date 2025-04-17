# File: models/escrow_tracker.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class EscrowTracker(Base):
    __tablename__ = "escrow_trackers"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    status = Column(String, default="initiated")
    amount_held = Column(Float)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
