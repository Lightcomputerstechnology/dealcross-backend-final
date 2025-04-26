from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum

class KYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class KYCRequest(Base):
    __tablename__ = "kyc_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    status = Column(Enum(KYCStatus), default=KYCStatus.pending)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
