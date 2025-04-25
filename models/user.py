from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from datetime import datetime
from core.database import Base  # ✅ Correct import
import enum
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # ✅ Add this for redeclaration issues

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cumulative_sales = Column(Numeric(12, 2), default=0.00)

    # Relationships
    fee_transactions = relationship("FeeTransaction", back_populates="user")
    fraud_alerts = relationship("FraudAlert", back_populates="user")