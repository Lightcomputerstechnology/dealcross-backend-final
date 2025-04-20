# File: schemas/metric.py

from pydantic import BaseModel
from datetime import datetime

class MetricOut(BaseModel):
    id: int
    type: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True
