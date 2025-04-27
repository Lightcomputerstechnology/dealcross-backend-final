# File: models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from core.database import Base

class UserRole(str, enum.Enum):
    user      = "user"
    moderator = "moderator"
    auditor   = "auditor"
    admin     = "admin"

class User(Base):
    __tablename__ = "users"

    id               = Column(Integer, primary_key=True, index=True)
    username         = Column(String,  unique=True, index=True, nullable=False)
    email            = Column(String,  unique=True, index=True, nullable=False)
    full_name        = Column(String,  nullable=True)
    hashed_password  = Column(String,  nullable=False)
    role             = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    status           = Column(String, default="active", nullable=False)
    tier             = Column(String, default="basic", nullable=False)
    cumulative_sales = Column(Numeric(12, 2), default=0.00)
    created_at       = Column(DateTime, default=datetime.utcnow)

    # … your other relationships here …

    # now unambiguous—SQLA knows KYCRequest.user_id → users.id
    kyc_requests = relationship(
        "KYCRequest",
        back_populates="user",
        cascade="all, delete-orphan"
    )