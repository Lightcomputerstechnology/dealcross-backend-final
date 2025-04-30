# File: schemas/chart.py

from datetime import datetime
from pydantic import BaseModel
from typing import List


# ─────────── Single Chart Point Creation ───────────
class ChartPointCreate(BaseModel):
    label: str
    value: float


# ─────────── Output Model for Single Point ───────────
class ChartPointOut(ChartPointCreate):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}


# ─────────── Grouped Response Schema ───────────
class ChartPoint(BaseModel):
    label: str         # e.g. "Mon", "Tue"
    value: float       # count (e.g. number of users/deals)
    timestamp: datetime


class ChartDataResponse(BaseModel):
    chart_type: str                  # e.g. "user_vs_deal"
    data: List[ChartPoint]