# File: app/api/routes/auditlog.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/audit-log")
def get_audit_log():
    return [
        {"id": 1, "action": "Deal created", "user": "admin", "timestamp": datetime.utcnow()},
        {"id": 2, "action": "User banned", "user": "moderator", "timestamp": datetime.utcnow()},
    ]
