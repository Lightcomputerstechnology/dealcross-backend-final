# File: schemas/chart.py

from pydantic import BaseModel
from typing import List
from datetime import datetime


class ChartPoint(BaseModel):
    label: str
    value: int
    timestamp: datetime


class ChartDataResponse(BaseModel):
    chart_type: str
    data: List[ChartPoint]

    class Config:
        orm_mode = True
