from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from core.database import Base

class ChartPoint(Base):
    __tablename__ = "chart_points"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)  # Example: "User Growth", "Revenue"
    value = Column(Float, nullable=False)   # Example: 1500.5
    timestamp = Column(DateTime, default=datetime.utcnow)  # Time of data point
