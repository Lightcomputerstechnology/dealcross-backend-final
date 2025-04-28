Chart Data Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends from datetime import datetime, timedelta from models.deal import Deal from models.user import User from schemas.chart import ChartDataResponse, ChartPoint

router = APIRouter()

@router.get("/chart-data", response_model=ChartDataResponse) async def get_chart_data(): today = datetime.utcnow() past_7_days = [today - timedelta(days=i) for i in reversed(range(7))]

user_data = []
deal_data = []

for day in past_7_days:
    day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)

    user_count = await User.filter(created_at__range=[day_start, day_end]).count()
    deal_count = await Deal.filter(created_at__range=[day_start, day_end]).count()

    user_data.append(ChartPoint(label=day.strftime("%a"), value=user_count, timestamp=day))
    deal_data.append(ChartPoint(label=day.strftime("%a"), value=deal_count, timestamp=day))

return ChartDataResponse(
    chart_type="user_vs_deal",
    data=user_data + deal_data
)

