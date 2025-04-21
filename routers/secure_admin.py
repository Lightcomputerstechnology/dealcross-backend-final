# File: routers/secure_admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_admin
from models.user import User

router = APIRouter()

@router.get("/secure-stats")
def secure_stats(admin_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return {
        "message": f"Welcome, admin {admin_user.username}",
        "role": "admin",
        "secure_data": {
            "access_level": "superuser",
            "admin_dashboard": True
        }
    }
