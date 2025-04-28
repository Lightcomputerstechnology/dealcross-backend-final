from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = {'extend_existing': True}  # Allow table reuse

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance = Column(Numeric(12, 2), default=0.00)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to User
    user = relationship(
        "User",
        back_populates="wallet",
        foreign_keys=[user_id]
    )
