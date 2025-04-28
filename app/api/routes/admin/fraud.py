# File: app/api/routes/admin/fraud.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.fraud import FraudAlert
from schemas.fraud import FraudAlertOut
from core.security import get_current_user

router = APIRouter(prefix="/admin/fraud", tags=["Admin - Fraud Reports"])

# === Get latest fraud reports ===
@router.get("/fraud-reports", response_model=List[FraudAlertOut])
async def get_fraud_reports(current_user=Depends(get_current_user)):
    """
    Fetch the 10 most recent fraud alerts.
    """
    try:
        fraud_alerts = await FraudAlert.all().order_by("-created_at").limit(10)
        return fraud_alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve fraud reports: {str(e)}")
