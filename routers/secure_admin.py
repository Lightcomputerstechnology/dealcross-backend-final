# File: routers/secure_admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from core.security import get_current_user
from typing import List

router = APIRouter()

@router.get("/admin-only")
def secure_admin_route(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Welcome Admin {current_user.username}"}


@router.get("/users/all", response_model=List[dict])
def list_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")

    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "status": u.status,
            "created_at": u.created_at
        }
        for u in users
    ]
    
