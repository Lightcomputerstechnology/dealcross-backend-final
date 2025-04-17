# File: src/models/aiinsight.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id         = Column(Integer, primary_key=True, index=True)
    content    = Column(String,  nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
