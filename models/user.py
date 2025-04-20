# File: models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False)   # Marks if user has admin privileges
    status = Column(String, default="active")   # Status: active, banned, pending, etc.

    created_at = Column(DateTime, default=datetime.utcnow)
