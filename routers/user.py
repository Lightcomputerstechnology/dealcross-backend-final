from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.exceptions import DoesNotExist
from typing import List

from core.security import get_current_user, get_password_hash
from schemas.user import UserOut, UserUpdate, UserAdminUpdate
from models.user import User, UserRole

router = APIRouter(prefix="/user", tags=["User Management"])


# === Current User Profile ===
@router.get("/profile", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return await UserOut.from_tortoise_orm(current_user)


@router.put("/profile/update", response_model=UserOut)
async def update_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    for field, value in updates.model_dump(exclude_unset=True).items():
        if field == "password":
            setattr(current_user, "hashed_password", get_password_hash(value))
        else:
            setattr(current_user, field, value)

    await current_user.save()
    return await UserOut.from_tortoise_orm(current_user)


# === User Fee Settings ===
@router.get("/settings")
async def get_user_settings(current_user: User = Depends(get_current_user)):
    tier = current_user.role.value if isinstance(current_user.role, UserRole) else current_user.role
    fee_rates = {
        "funding":      "2%" if tier == "basic" else "1.5%",
        "escrow":       "3%" if tier == "basic" else "2%",
        "share_buyer":  "2%" if tier == "basic" else "1.5%",
        "share_seller": "1% (after $1,000)" if tier == "basic" else "0.75% (after $1,000)",
    }

    return {
        "message": "User settings retrieved successfully",
        "data": {
            "user_id": current_user.id,
            "tier": tier,
            "fee_rates": fee_rates,
        }
    }


# === Admin: List All Users ===
@router.get("/admin/users", response_model=List[UserOut])
async def list_users(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return [await UserOut.from_tortoise_orm(u) for u in await User.all()]


# === Admin: Update Any User ===
@router.put("/admin/update/{user_id}", response_model=UserOut)
async def admin_update_user(
    user_id: int,
    updates: UserAdminUpdate,
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await user.save()
    return await UserOut.from_tortoise_orm(user)