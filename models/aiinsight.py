from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
from datetime import datetime

class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    insight = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
