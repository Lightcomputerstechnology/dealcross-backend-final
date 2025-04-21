# File: app/api/routes/admin/fraud.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.fraud import FraudAlert
from schemas.fraud import FraudAlertOut

router = APIRouter()

@router.get("/fraud-reports", response_model=List[FraudAlertOut])
def get_fraud_reports(db: Session = Depends(get_db)):
    """
    Fetch the 10 most recent fraud alerts.
    """
    try:
        return (
            db.query(FraudAlert)
            .order_by(FraudAlert.created_at.desc())
            .limit(10)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve fraud reports: {str(e)}")
