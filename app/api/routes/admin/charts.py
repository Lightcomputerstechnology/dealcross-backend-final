# File: app/api/routes/admin/charts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import List, Dict
from core.database import get_db
from models.deal import Deal
from models.user import User
from models.fraud import FraudAlert

router = APIRouter()

@router.get("/admin/charts", response_model=List[Dict])
def get_chart_data(db: Session = Depends(get_db)):
    """
    Provides data for admin charts:
    - Daily count of new users
    - Daily count of new deals
    - Daily count of fraud alerts
    """
    today = datetime.utcnow().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    def count_records(model):
        results = (
            db.query(func.date(model.created_at).label("date"), func.count().label("count"))
            .filter(model.created_at >= today - timedelta(days=6))
            .group_by(func.date(model.created_at))
            .all()
        )
        return {record.date: record.count for record in results}

    try:
        users_data = count_records(User)
        deals_data = count_records(Deal)
        fraud_data = count_records(FraudAlert)

        chart_data = []
        for date in last_7_days:
            chart_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "users": users_data.get(date, 0),
                "deals": deals_data.get(date, 0),
                "frauds": fraud_data.get(date, 0),
            })

        return chart_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate chart data: {str(e)}")
