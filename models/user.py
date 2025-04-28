from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from core.database import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)

    # Relationships
    kyc_requests = relationship("KYCRequest", back_populates="user", foreign_keys="KYCRequest.user_id")
    reviewed_kyc_requests = relationship("KYCRequest", back_populates="reviewer", foreign_keys="KYCRequest.reviewed_by")
