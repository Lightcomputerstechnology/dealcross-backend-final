from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.exceptions import DoesNotExist
from typing import List

from core.security import get_current_user, get_password_hash
from schemas.user import UserOut, UserUpdate, UserAdminUpdate
from models.user import User, UserRole

router = APIRouter(prefix="/user", tags=["User Management"])


# === View Current User Profile ===
@router.get(
    "/profile",
    response_model=UserOut,
    summary="Get current user profile"
)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    return await UserOut.from_tortoise_orm(current_user)


# === Update Current User Profile ===
@router.put(
    "/profile/update",
    response_model=UserOut,
    summary="Update current user profile"
)
async def update_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    if updates.username is not None:
        current_user.username = updates.username
    if updates.email is not None:
        current_user.email = updates.email
    if updates.password is not None:
        current_user.hashed_password = get_password_hash(updates.password)
    if updates.full_name is not None:
        current_user.full_name = updates.full_name

    await current_user.save()
    return await UserOut.from_tortoise_orm(current_user)


# === Get User Settings (Fees & Tier) ===
@router.get(
    "/settings",
    summary="View user tier and fee rates"
)
async def get_user_settings(
    current_user: User = Depends(get_current_user)
):
    tier = (
        current_user.role.value
        if isinstance(current_user.role, UserRole)
        else current_user.role
    )
    fee_rates = {
        "funding":      "2%" if tier == "basic" else "1.5%",
        "escrow":       "3%" if tier == "basic" else "2%",
        "share_buyer":  "2%" if tier == "basic" else "1.5%",
        "share_seller": "1% (after $1,000)" if tier == "basic" else "0.75% (after $1,000)",
    }
    return {
        "message": "User settings retrieved successfully",
        "data": {
            "user_id":   current_user.id,
            "tier":      tier,
            "fee_rates": fee_rates,
        },
    }


# === Admin: List All Users ===
@router.get(
    "/admin/users",
    response_model=List[UserOut],
    summary="Admin: List all users"
)
async def list_users(
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    users = await User.all()
    return [await UserOut.from_tortoise_orm(u) for u in users]


# === Admin: Update User Role / Status ===
@router.put(
    "/admin/update/{user_id}",
    response_model=UserOut,
    summary="Admin: Update user role or status"
)
async def admin_update_user(
    user_id: int,
    updates: UserAdminUpdate,
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if updates.username is not None:
        user.username = updates.username
    if updates.email is not None:
        user.email = updates.email
    if updates.role is not None:
        user.role = updates.role
    if updates.status is not None:
        user.status = updates.status
    if updates.full_name is not None:
        user.full_name = updates.full_name

    await user.save()
    return await UserOut.from_tortoise_orm(user)
    
