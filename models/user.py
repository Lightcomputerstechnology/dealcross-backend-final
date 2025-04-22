# File: models/user.py

from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
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
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.user)  # ✅ Replaces is_admin
    status = Column(String, default="active")  # active, banned, pending, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
