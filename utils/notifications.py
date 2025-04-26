File: src/utils/notifications.py

from sqlalchemy.orm import Session from models.notification import Notification from fastapi import BackgroundTasks from core.email_utils import send_email

def create_notification( db: Session, user_id: int, title: str, message: str ) -> Notification: """ Creates an in-app notification for the specified user and returns it. """ notification = Notification( user_id=user_id, title=title, message=message ) db.add(notification) db.commit() db.refresh(notification) return notification

def send_email_notification( background_tasks: BackgroundTasks, to_email: str, subject: str, body: str ) -> None: """ Schedules an email to be sent in the background using FastAPI's BackgroundTasks. """ background_tasks.add_task(send_email, to_email, subject, body)

def notify_user( db: Session, background_tasks: BackgroundTasks, user_id: int, title: str, message: str, email_subject: str, email_body: str ) -> Notification: """ Convenience helper to create an in-app notification and send an email notification at once. Returns the created Notification object. """ # Create in-app notification notification = create_notification(db, user_id, title, message)

# Fetch user's email for sending
from sqlalchemy.orm import Session as _Session  # prevent circular import
user = db.query(Notification).filter(Notification.id == notification.id).first()
# Schedule email in background
send_email_notification(background_tasks, user.email, email_subject, email_body)

return notification

