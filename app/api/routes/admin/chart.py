File: app/api/routes/admin/chart.py

from fastapi import APIRouter, Depends, HTTPException from sqlalchemy.orm import Session from sqlalchemy.sql import func from core.database import get_db from models.deal import Deal from models.user import User from models.fraud import FraudAlert from datetime import datetime, timedelta from typing import List, Dict

router = APIRouter()

@router.get("/metrics/chart", response_model=List[Dict]) def get_chart_data(db: Session = Depends(get_db)): try: today = datetime.utcnow().date() last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

def count_records(model):
        return (
            db.query(func.date(model.created_at), func.count())
            .filter(model.created_at >= today - timedelta(days=6))
            .group_by(func.date(model.created_at))
            .all()
        )

    users_data = dict(count_records(User))
    deals_data = dict(count_records(Deal))
    fraud_data = dict(count_records(FraudAlert))

    chart_data = []
    for date in last_7_days:
        label = date.strftime("%a")
        chart_data.append({
            "label": label,
            "users": users_data.get(date, 0),
            "deals": deals_data.get(date, 0),
            "frauds": fraud_data.get(date, 0),
        })

    return chart_data

except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

