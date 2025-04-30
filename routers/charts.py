# File: routers/chart.py

from fastapi import APIRouter
from datetime import datetime, timedelta
from models.user import User
from models.deal import Deal
from schemas.chart import ChartDataResponse, ChartPoint

router = APIRouter(prefix="/charts", tags=["Charts"])

@router.get("/user-vs-deal", response_model=ChartDataResponse, summary="Get user vs deal chart data")
async def get_user_vs_deal_chart():
    today = datetime.utcnow()
    past_7_days = [today - timedelta(days=i) for i in reversed(range(7))]

    data_points = []

    for day in past_7_days:
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)

        user_count = await User.filter(created_at__range=[day_start, day_end]).count()
        deal_count = await Deal.filter(created_at__range=[day_start, day_end]).count()

        data_points.append(ChartPoint(label=day.strftime("%a"), value=user_count, timestamp=day))
        data_points.append(ChartPoint(label=f"{day.strftime('%a')} (Deals)", value=deal_count, timestamp=day))

    return ChartDataResponse(
        chart_type="user_vs_deal",
        data=data_points
    )