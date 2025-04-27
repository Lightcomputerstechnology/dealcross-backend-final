from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
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

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships - ALL WITH foreign_keys clarification
    kyc_requests = relationship("KYCRequest", back_populates="user", foreign_keys="KYCRequest.user_id")
    created_deals = relationship("Deal", back_populates="creator", foreign_keys="Deal.creator_id")
    counterparty_deals = relationship("Deal", back_populates="counterparty", foreign_keys="Deal.counterparty_id")
