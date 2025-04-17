from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Optional: if you want reverse relationships (not necessary for now)
    # deals_created = relationship("Deal", foreign_keys='Deal.creator_id')
    # deals_received = relationship("Deal", foreign_keys='Deal.counterparty_id')
