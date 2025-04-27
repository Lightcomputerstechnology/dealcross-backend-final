from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from core.database import Base

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Avoid duplicate table errors

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    kyc_requests = relationship(
        "KYCRequest",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="[KYCRequest.user_id]"
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,  # One-to-one relationship
        cascade="all, delete",
        foreign_keys="[Wallet.user_id]"
    )