# File: routers/admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from models.deal import Deal
from models.dispute import Dispute
from core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def list_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    users = db.query(User).all()
    return [
        {
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "status": "active"
        } for u in users
    ]

@router.get("/analytics")
def analytics_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "users": db.query(User).count(),
        "deals": db.query(Deal).count(),
        "wallets_funded": db.query(User).filter(User.wallet_balance > 0).count(),
        "disputes": db.query(Dispute).count()
    }
