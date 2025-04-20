# File: schemas/metrics.py

from datetime import datetime
from pydantic import BaseModel

# For individual metric entries (e.g. chart points)
class MetricEntry(BaseModel):
    id: int
    type: str
    value: int
    timestamp: datetime

    class Config:
        from_attributes = True

# For chart series data (bar/line chart)
class ChartSeriesData(BaseModel):
    label: str
    data: list[int]
    timestamps: list[str]
