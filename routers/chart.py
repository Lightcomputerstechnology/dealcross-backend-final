# File: routers/chart.py

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from tortoise.expressions import Q
from models.chart import ChartPoint
from core.security import get_current_admin

router = APIRouter(prefix="/admin/charts", tags=["Admin Charts"])


@router.get("/", summary="Get admin chart data")
async def get_chart_data(
    days: int = Query(30, ge=1, le=90),
    admin: dict = Depends(get_current_admin)
):
    """
    Returns chart data from the past `days` number of days, grouped by label.
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    points = await ChartPoint.filter(timestamp__gte=cutoff).order_by("timestamp")

    grouped = {}
    for point in points:
        grouped.setdefault(point.label, []).append({
            "label": point.timestamp.strftime("%b %d"),
            "value": point.value
        })

    return grouped