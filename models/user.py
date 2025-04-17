from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from core.database import Base

class AppSettings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
