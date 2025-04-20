# File: app/api/routes/admin/fraud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.fraud import FraudAlert
from schemas.fraud import FraudAlertOut
from typing import List

router = APIRouter()

@router.get("/fraud-reports", response_model=List[FraudAlertOut])
def get_fraud_reports(db: Session = Depends(get_db)):
    try:
        reports = db.query(FraudAlert).order_by(FraudAlert.created_at.desc()).limit(10).all()
        return reports
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching fraud reports")

