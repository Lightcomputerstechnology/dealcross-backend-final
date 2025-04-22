# File: routers/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db  # ✅ Use shared DB dependency
from models.user import User
from models.deal import Deal
from models.dispute import Dispute
from core.dependencies import require_admin  # ✅ Admin check

router = APIRouter()

@router.get("/users")
def list_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):  # ✅ Protect with require_admin
    users = db.query(User).all()
    return [
        {
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "status": u.status
        } for u in users
    ]

@router.get("/analytics")
def analytics_summary(db: Session = Depends(get_db), admin: User = Depends(require_admin)):  # ✅ Protect with require_admin
    return {
        "users": db.query(User).count(),
        "deals": db.query(Deal).count(),
        "wallets_funded": db.query(User).filter(User.wallet_balance > 0).count() if hasattr(User, "wallet_balance") else "N/A",
        "disputes": db.query(Dispute).count()
    }
