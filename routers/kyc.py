# File: src/models/kyc.py

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum

class KYCStatus(str, enum.Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

class KYC(Base):
    __tablename__  = "kyc_requests"
    __table_args__ = {"extend_existing": True}

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String, nullable=False)
    document_url  = Column(String, nullable=False)
    status        = Column(Enum(KYCStatus), default=KYCStatus.pending, nullable=False)
    submitted_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

    # ——— Admin review fields ———
    review_note   = Column(Text,     nullable=True)
    reviewed_by   = Column(Integer,  ForeignKey("users.id"), nullable=True)
    reviewed_at   = Column(DateTime, nullable=True)

    # relationship back to User
    user = relationship("User", back_populates="kyc_requests")