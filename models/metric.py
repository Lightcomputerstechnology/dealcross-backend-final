# # File: models/metric.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from core.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)  # e.g., 'users', 'deals', 'wallets_funded'
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
