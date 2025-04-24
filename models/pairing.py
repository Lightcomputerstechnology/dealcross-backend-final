from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum

class PairingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"

class Pairing(Base):
    __tablename__ = "pairings"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    counterparty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(PairingStatus), default=PairingStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", foreign_keys=[creator_id])
    counterparty = relationship("User", foreign_keys=[counterparty_id])