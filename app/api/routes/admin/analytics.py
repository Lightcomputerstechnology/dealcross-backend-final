# File: app/api/routes/admin/analytics.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

class AdminMetric(BaseModel):
    id: int
    type: str
    value: float
    timestamp: datetime

# Simulated data (replace with real admin metrics logic)
admin_metrics = [
    {"id": 1, "type": "wallet", "value": 900, "timestamp": datetime.utcnow() - timedelta(minutes=15)},
    {"id": 2, "type": "fraud", "value": 1, "timestamp": datetime.utcnow() - timedelta(minutes=30)},
]

@router.get("/admin-metrics", response_model=List[AdminMetric])
def get_admin_metrics(
    type: Optional[str] = Query(None, description="Filter by type: wallet, fraud"),
    minutes: Optional[int] = Query(None, description="Last X minutes")
):
    data = admin_metrics
    if type:
        data = [m for m in data if m["type"] == type]
    if minutes:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        data = [m for m in data if m["timestamp"] >= cutoff]
    return data
