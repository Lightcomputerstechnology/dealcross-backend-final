# File: app/api/routes/dealcontrol.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/pending-deals")
def list_pending_deals():
    return [
        {"id": 1, "title": "Payment Escrow", "amount": 5000, "status": "pending", "created_at": datetime.utcnow()},
        {"id": 2, "title": "Car Sale", "amount": 8000, "status": "pending", "created_at": datetime.utcnow()},
    ]
