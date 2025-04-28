# Notifications Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user
from models.notification import Notification
from schemas.notification_schema import NotificationOut
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])  # ✅ Tag added

# === Get user notifications ===

@router.get("/my-notifications", response_model=List[NotificationOut], summary="Retrieve your notifications")
async def get_my_notifications(current_user=Depends(get_current_user)):
    return await Notification.filter(user=current_user).order_by("-created_at")

# === Mark notification as read ===

@router.put("/mark-read/{notification_id}", summary="Mark a notification as read")
async def mark_notification_as_read(
    notification_id: int,
    current_user=Depends(get_current_user)
):
    notification = await Notification.get_or_none(id=notification_id, user=current_user)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    await notification.save()
    return {"message": "Notification marked as read"}
