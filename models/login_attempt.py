# File: models/login_attempt.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from core.database import Base

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, nullable=False)  # 'failed' or 'successful'
    timestamp = Column(DateTime, default=datetime.utcnow)
