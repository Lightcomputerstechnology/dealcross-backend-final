# File: schemas/chart.py

from datetime import datetime
from pydantic import BaseModel
from typing import List

class ChartPoint(BaseModel):
    label: str         # e.g. "Mon", "Tue"
    value: int         # count (e.g. number of users/deals)
    timestamp: datetime

class ChartDataResponse(BaseModel):
    chart_type: str                  # e.g. "user_vs_deal"
    data: List[ChartPoint]
