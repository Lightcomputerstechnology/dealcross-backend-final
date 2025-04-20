# File: routers/charts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.metric import Metric
from schemas.metric import MetricOut
from typing import List

router = APIRouter()

@router.get("/charts", response_model=List[MetricOut])
def get_chart_data(db: Session = Depends(get_db)):
    try:
        # Fetch recent 20 metrics grouped by type
        metrics = db.query(Metric).order_by(Metric.timestamp.desc()).limit(20).all()
        return metrics
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load chart data.")
