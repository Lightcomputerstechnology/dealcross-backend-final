from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base  # ✅ Correct Base import

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    status = Column(String, default="active", nullable=False)
    tier = Column(String, default="basic", nullable=False)
    cumulative_sales = Column(Numeric(12, 2), default=0.00)

    # Relationships
    fee_transactions = relationship("FeeTransaction", back_populates="user")
    fraud_alerts = relationship("FraudAlert", back_populates="user")
    created_deals = relationship("Deal", back_populates="creator", foreign_keys="Deal.creator_id")
    counterparty_deals = relationship("Deal", back_populates="counterparty", foreign_keys="Deal.counterparty_id")
    wallet = relationship("Wallet", back_populates="user", uselist=False)