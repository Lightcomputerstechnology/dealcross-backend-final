# File: app/api/routes/analytics.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

class Metric(BaseModel):
    id: int
    type: str
    value: float
    timestamp: datetime

fake_metrics_data = [
    {"id": 1, "type": "deal", "value": 4200, "timestamp": datetime.utcnow() - timedelta(seconds=5)},
    {"id": 2, "type": "user", "value": 1, "timestamp": datetime.utcnow() - timedelta(seconds=10)},
    {"id": 3, "type": "wallet", "value": 900, "timestamp": datetime.utcnow() - timedelta(seconds=15)},
    {"id": 4, "type": "dispute", "value": 0, "timestamp": datetime.utcnow() - timedelta(seconds=20)},
    {"id": 5, "type": "fraud", "value": 1, "timestamp": datetime.utcnow() - timedelta(seconds=25)},
]

@router.get("/metrics", response_model=List[Metric])
def get_metrics(
    type: Optional[str] = Query(None, description="Filter by metric type"),
    since: Optional[int] = Query(None, description="Only metrics in the last X seconds")
):
    data = fake_metrics_data
    if type:
        data = [m for m in data if m["type"] == type]
    if since:
        cutoff = datetime.utcnow() - timedelta(seconds=since)
        data = [m for m in data if m["timestamp"] >= cutoff]
    return data
