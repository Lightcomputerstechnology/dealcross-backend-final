# File: routers/analytics.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

class PublicMetric(BaseModel):
    id: int
    type: str
    value: float
    timestamp: datetime

# Simulated data (replace with DB logic later)
public_metrics = [
    {"id": 1, "type": "deal", "value": 4200, "timestamp": datetime.utcnow() - timedelta(minutes=5)},
    {"id": 2, "type": "user", "value": 15, "timestamp": datetime.utcnow() - timedelta(minutes=10)},
]

@router.get("/public-metrics", response_model=List[PublicMetric])
def get_public_metrics(
    type: Optional[str] = Query(None, description="Filter by type: deal, user"),
    minutes: Optional[int] = Query(None, description="Last X minutes")
):
    data = public_metrics
    if type:
        data = [m for m in data if m["type"] == type]
    if minutes:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        data = [m for m in data if m["timestamp"] >= cutoff]
    return data
