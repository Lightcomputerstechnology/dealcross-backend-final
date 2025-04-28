# File: app/api/routes/admin/charts.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta
from models.user import User
from models.deal import Deal
from models.fraud import FraudAlert
from core.security import get_current_user

router = APIRouter(prefix="/admin/charts", tags=["Admin - Charts"])

@router.get("/", response_model=List[Dict])
async def get_chart_data(current_user=Depends(get_current_user)):
    """
    Provides data for admin charts:
    - Daily count of new users
    - Daily count of new deals
    - Daily count of fraud alerts
    """
    today = datetime.utcnow().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    def format_date(dt):
        return dt.strftime("%Y-%m-%d")

    try:
        users = await User.all()
        deals = await Deal.all()
        frauds = await FraudAlert.all()

        users_data = {}
        deals_data = {}
        fraud_data = {}

        for user in users:
            date = format_date(user.created_at.date())
            users_data[date] = users_data.get(date, 0) + 1

        for deal in deals:
            date = format_date(deal.created_at.date())
            deals_data[date] = deals_data.get(date, 0) + 1

        for fraud in frauds:
            date = format_date(fraud.created_at.date())
            fraud_data[date] = fraud_data.get(date, 0) + 1

        chart_data = []
        for date in last_7_days:
            formatted = date.strftime("%Y-%m-%d")
            chart_data.append({
                "date": formatted,
                "users": users_data.get(formatted, 0),
                "deals": deals_data.get(formatted, 0),
                "frauds": fraud_data.get(formatted, 0),
            })

        return chart_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate chart data: {str(e)}")
