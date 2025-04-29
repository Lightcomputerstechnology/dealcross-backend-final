# File: app/api/routes/admin/analytics.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin/analytics", tags=["Admin - Analytics"])

class AdminMetric(BaseModel):
    id: int
    type: str
    value: float
    timestamp: datetime

# Simulated static metrics (placeholder)
admin_metrics = [
    {"id": 1, "type": "wallet", "value": 900.0, "timestamp": datetime.utcnow() - timedelta(minutes=15)},
    {"id": 2, "type": "fraud", "value": 1.0, "timestamp": datetime.utcnow() - timedelta(minutes=30)},
]

@router.get("/metrics", response_model=List[AdminMetric])
async def get_admin_metrics(
    type: Optional[str] = Query(None, description="Filter by type (e.g., wallet, fraud)"),
    minutes: Optional[int] = Query(None, description="Only return data from the last X minutes")
):
    """
    Retrieve platform-wide admin metrics for analytics dashboard.
    """
    data = admin_metrics
    if type:
        data = [m for m in data if m["type"] == type]
    if minutes:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        data = [m for m in data if m["timestamp"] >= cutoff]
    return data
