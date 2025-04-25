from sqlalchemy import Column, Integer, Numeric
from core.database import Base

class AdminWallet(Base):
    __tablename__ = "admin_wallet"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Numeric(12, 2), default=0.00)