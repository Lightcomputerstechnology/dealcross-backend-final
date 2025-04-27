# File: routers/charts.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from datetime import datetime, timedelta
from models.deal import Deal
from models import User
from schemas.chart import ChartDataResponse, ChartPoint

router = APIRouter()

@router.get("/chart-data", response_model=ChartDataResponse)
def get_chart_data(db: Session = Depends(get_db)):
    today = datetime.utcnow()
    past_7_days = [today - timedelta(days=i) for i in reversed(range(7))]

    user_data = []
    deal_data = []

    for day in past_7_days:
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)

        user_count = db.query(User).filter(User.created_at.between(day_start, day_end)).count()
        deal_count = db.query(Deal).filter(Deal.created_at.between(day_start, day_end)).count()

        user_data.append(ChartPoint(label=day.strftime("%a"), value=user_count, timestamp=day))
        deal_data.append(ChartPoint(label=day.strftime("%a"), value=deal_count, timestamp=day))

    return ChartDataResponse(
        chart_type="user_vs_deal",
        data=user_data + deal_data
        )
