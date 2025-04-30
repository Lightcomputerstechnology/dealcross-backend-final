# File: schemas/chart.py

from datetime import datetime
from pydantic import BaseModel
from typing import List


# ─────────── Single Chart Point Creation ───────────
class ChartPointCreate(BaseModel):
    label: str         # e.g., "Mon", "Revenue"
    value: float       # Numeric metric


# ─────────── Output Model for a Saved Chart Point ───────────
class ChartPointOut(ChartPointCreate):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}


# ─────────── Reusable Data Point Model for Charts ───────────
class ChartPoint(BaseModel):
    label: str                  # e.g., "Mon", "Tue"
    value: float                # User or deal count
    timestamp: datetime


# ─────────── Full Response Payload for Chart API ───────────
class ChartDataResponse(BaseModel):
    chart_type: str             # e.g., "user_vs_deal", "growth_over_time"
    data: List[ChartPoint]