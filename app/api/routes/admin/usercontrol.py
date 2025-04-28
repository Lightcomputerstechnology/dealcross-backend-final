# File: src/app/api/routes/admin/usercontrol.py

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
from models.user import User
from schemas.user import UserOut, UserAdminUpdate
from core.security import get_current_user

router = APIRouter(prefix="/admin/usercontrol", tags=["Admin - User Control"])

# === List all users ===
@router.get("/all-users", response_model=List[UserOut])
async def list_all_users(current_user=Depends(get_current_user)):
    users = await User.all().order_by("-created_at")
    return users

# === Update user by admin ===
@router.put("/update-user/{user_id}", response_model=UserOut)
async def update_user_admin(
    user_id: int,
    update: UserAdminUpdate,
    current_user=Depends(get_current_user)
):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update.is_active is not None:
        user.status = "active" if update.is_active else "inactive"
    if update.is_banned is not None:
        user.is_banned = update.is_banned
        if update.is_banned:
            user.status = "banned"
    if update.ban_reason is not None:
        user.ban_reason = update.ban_reason
    if update.approval_note is not None:
        user.approval_note = update.approval_note

    await user.save()
    return user

# === Ban a user ===
@router.put("/ban-user/{user_id}")
async def ban_user(
    user_id: int,
    reason: Optional[str] = Body(None, embed=True),
    current_user=Depends(get_current_user)
):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_banned = True
    user.status = "banned"
    user.ban_reason = reason or "Banned by admin"
    await user.save()
    return {"message": f"User {user.username} has been banned."}

# === Unban a user ===
@router.put("/unban-user/{user_id}")
async def unban_user(user_id: int, current_user=Depends(get_current_user)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_banned = False
    user.status = "active"
    user.ban_reason = None
    await user.save()
    return {"message": f"User {user.username} has been unbanned."}

# === Approve a user ===
@router.post("/approve-user/{user_id}")
async def approve_user(
    user_id: int,
    note: Optional[str] = Body(None, embed=True),
    current_user=Depends(get_current_user)
):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = "active"
    user.approval_note = note or "Approved by admin"
    await user.save()
    return {"message": f"User {user.username} has been approved."}
