from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, get_password_hash
from models.user import User
from schemas.user import UserOut, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["User Profile"],
)

# ───────────── GET CURRENT USER PROFILE ─────────────
@router.get("/me", response_model=UserOut)
def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# ───────────── UPDATE CURRENT USER PROFILE ─────────────
@router.put("/me", response_model=UserOut)
def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if update_data.full_name:
        current_user.full_name = update_data.full_name

    if update_data.password:
        current_user.hashed_password = get_password_hash(update_data.password)

    db.commit()
    db.refresh(current_user)
    return current_user