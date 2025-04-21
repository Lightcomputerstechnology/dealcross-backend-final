from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from schemas.user import UserOut, UserAdminUpdate
from typing import List

router = APIRouter()

@router.get("/all-users", response_model=List[UserOut])
def list_all_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


@router.put("/update-user/{user_id}", response_model=UserOut)
def update_user_admin(
    user_id: int,
    update: UserAdminUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update.is_active is not None:
        user.is_active = update.is_active
    if update.is_banned is not None:
        user.is_banned = update.is_banned
    if update.ban_reason is not None:
        user.ban_reason = update.ban_reason
    if update.approval_note is not None:
        user.approval_note = update.approval_note

    db.commit()
    db.refresh(user)
    return user


@router.put("/ban-user/{user_id}")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_banned = True
    db.commit()
    return {"message": f"User {user_id} has been banned."}


@router.put("/unban-user/{user_id}")
def unban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_banned = False
    user.ban_reason = None
    db.commit()
    return {"message": f"User {user_id} has been unbanned."}
