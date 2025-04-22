# File: utils/notifications.py

from sqlalchemy.orm import Session
from models.notification import Notification

def create_notification(db: Session, user_id: int, title: str, message: str):
    """
    Creates an in-app notification for the specified user.
    """
    notification = Notification(
        user_id=user_id,
        title=title,          # ✅ Includes title
        message=message
    )
    db.add(notification)
    db.commit()
