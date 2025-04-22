# File: core/dependencies.py

from fastapi import Depends, HTTPException, status
from core.security import get_current_user
from models.user import User

def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user
