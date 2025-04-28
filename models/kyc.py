# models/kyc.py

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class KYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCRequest(Base):
    __tablename__ = "kyc_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    status = Column(Enum(KYCStatus), default=KYCStatus.pending, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime)

    # Back-populates for SQLAlchemy relationship
    user = relationship("User", back_populates="kyc_requests")
