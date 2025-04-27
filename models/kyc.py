from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class KYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCRequest(Base):
    __tablename__ = "kyc_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    document_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    status = Column(Enum(KYCStatus), default=KYCStatus.pending)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to User WITH foreign_keys clarification
    user = relationship("User", back_populates="kyc_requests", foreign_keys=[user_id])
