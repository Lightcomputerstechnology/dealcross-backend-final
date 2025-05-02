# routers/chart.py

from fastapi import APIRouter, Depends
from core.security import get_current_user
from models.user import User
from models.chart import ChartPoint
from schemas.chart import ChartPointOut

router = APIRouter(prefix="/chart", tags=["Chart"])


# Fetch all chart points for dashboard
@router.get("/", response_model=list[ChartPointOut])
async def get_chart_data(current_user: User = Depends(get_current_user)):
    return await ChartPoint.all().order_by("-created_at")
