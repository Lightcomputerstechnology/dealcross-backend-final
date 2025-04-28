from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
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

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    status = Column(Enum(KYCStatus), default=KYCStatus.pending, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    review_note = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship(
    "User",
    back_populates="kyc_requests",
    foreign_keys="[user_id]"
)

reviewer = relationship(
    "User",
    back_populates="reviewed_kyc_requests",
    foreign_keys="[reviewed_by]"
)
