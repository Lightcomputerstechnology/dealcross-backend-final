# File: app/api/routes/usercontrol.py
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/user-controls")
def get_users():
    return [
        {"id": 1, "username": "john_doe", "email": "john@example.com", "status": "active", "joined": datetime.utcnow()},
        {"id": 2, "username": "jane_smith", "email": "jane@example.com", "status": "banned", "joined": datetime.utcnow()},
    ]
