# File: models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from core.database import Base  # ✅ Correct Base import
from models.wallet import Wallet  # ✅ Import Wallet to reference its foreign key

# User role definitions
class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

# User model
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
    created_at = Column(DateTime, default=datetime.utcnow)  # Optional timestamp

    # Relationships
    fee_transactions = relationship("FeeTransaction", back_populates="user")
    fraud_alerts = relationship("FraudAlert", back_populates="user")
    created_deals = relationship("Deal", back_populates="creator", foreign_keys="Deal.creator_id")
    counterparty_deals = relationship("Deal", back_populates="counterparty", foreign_keys="Deal.counterparty_id")

    # ✅ Wallet relationship with explicit foreign_keys
    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,
        foreign_keys="[Wallet.user_id]"
    )
