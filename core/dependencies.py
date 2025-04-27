# File: core/dependencies.py

from fastapi import Depends, HTTPException, status
from core.security import get_current_user
from models import User  # ✅ Import roles

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user

def require_moderator(user: User = Depends(get_current_user)) -> User:
    if user.role not in [UserRole.admin, UserRole.moderator]:
        raise HTTPException(status_code=403, detail="Moderator access required.")
    return user

def require_auditor(user: User = Depends(get_current_user)) -> User:
    if user.role not in [UserRole.admin, UserRole.auditor]:
        raise HTTPException(status_code=403, detail="Auditor access required.")
    return user
