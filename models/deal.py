# File: models/deal.py

from core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql import func

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Float)
    escrow_type = Column(String)
    role = Column(String)
    status = Column(String, default="Pending")
    creator_id = Column(Integer, ForeignKey("users.id"))
    counterparty_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
