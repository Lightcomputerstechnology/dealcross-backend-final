from sqlalchemy import Column, Integer, Numeric, DateTime
from datetime import datetime
from core.database import Base

class AdminWallet(Base):
    __tablename__ = "admin_wallet"
    __table_args__ = {'extend_existing': True}  # Allow table reuse

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Numeric(12, 2), default=0.00)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
