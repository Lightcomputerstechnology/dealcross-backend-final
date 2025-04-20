# File: app/api/routes/admin/fraud.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/fraud-reports")
async def get_fraud_reports():
    return [
        {"id": 1, "message": "Unusual withdrawal by user A", "timestamp": "2025-04-20T15:30:00Z"},
        {"id": 2, "message": "Multiple login attempts from different IPs - user B", "timestamp": "2025-04-20T15:25:00Z"},
        {"id": 3, "message": "Transaction reversal flagged - user C", "timestamp": "2025-04-20T15:20:00Z"}
    ]
