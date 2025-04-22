# File: routers/notifications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.notification import Notification
from schemas.notification_schema import NotificationOut
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])  # ✅ Tag added

# === Get user notifications ===
@router.get("/my-notifications", response_model=List[NotificationOut], summary="Retrieve your notifications")
def get_my_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieves all notifications for the logged-in user, ordered by the most recent.

    - **Returns**: List of notifications with their read/unread status.
    """
    return db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()

# === Mark notification as read ===
@router.put("/mark-read/{notification_id}", summary="Mark a notification as read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Marks a specific notification as read.

    - **notification_id**: ID of the notification to mark as read.
    """
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}
