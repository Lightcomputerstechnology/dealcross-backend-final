User Profile Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from core.security import get_current_user, get_password_hash from models.user import User from schemas.user import UserOut, UserUpdate

router = APIRouter( prefix="/users", tags=["User Profile"], )

───────────── GET CURRENT USER PROFILE ─────────────

@router.get("/me", response_model=UserOut) async def read_my_profile(current_user: User = Depends(get_current_user)): return current_user

───────────── UPDATE CURRENT USER PROFILE ─────────────

@router.put("/me", response_model=UserOut) async def update_my_profile( update_data: UserUpdate, current_user: User = Depends(get_current_user) ): if update_data.full_name: current_user.full_name = update_data.full_name

if update_data.password:
    current_user.hashed_password = get_password_hash(update_data.password)

await current_user.save()
return current_user

