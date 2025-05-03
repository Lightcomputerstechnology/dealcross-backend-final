from fastapi import APIRouter, HTTPException
from models.user import User
from schemas.user import UserOut
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
async def list_users():
    users = await User.all()
    return [await UserOut.from_tortoise_orm(u) for u in users]

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await UserOut.from_tortoise_orm(user)
