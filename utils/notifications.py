File: src/utils/notifications.py

from sqlalchemy.orm import Session from models.notification import Notification from fastapi import BackgroundTasks from core.email_utils import send_email  # send_email helper

def create_notification( db: Session, user_id: int, title: str, message: str ) -> Notification: """ Creates an in-app notification for the specified user. """ notification = Notification( user_id=user_id, title=title, message=message ) db.add(notification) db.commit() db.refresh(notification) return notification

def send_email_notification( background_tasks: BackgroundTasks, to_email: str, subject: str, body: str ) -> None: """ Schedules an email to be sent in the background. """ background_tasks.add_task(send_email, to_email, subject, body)

