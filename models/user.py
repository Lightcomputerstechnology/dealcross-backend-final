from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from datetime import datetime
from core.database import Base
import enum
from sqlalchemy.orm import relationship  # Added for relationship

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

    # ✅ Added for monetization tracking
    cumulative_sales = Column(Numeric(12, 2), default=0.00)

    # ✅ Fee transactions relationship
    fee_transactions = relationship("FeeTransaction", back_populates="user")
