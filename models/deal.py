# File: models/deal.py

from sqlalchemy import Column, String, Integer, Float, Boolean
from core.database import Base

class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default='pending')
    counterparty_email = Column(String, nullable=False)
    description = Column(String, nullable=True)
    public_deal = Column(Boolean, default=False)  # NEW: Public visibility flag
