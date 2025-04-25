File: models/notification.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime from datetime import datetime from core.database import Base

class Notification(Base): tablename = "notifications"

id = Column(Integer, primary_key=True, index=True)
user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
title = Column(String, nullable=False)
message = Column(String, nullable=False)
is_read = Column(Boolean, default=False)
created_at = Column(DateTime, default=datetime.utcnow)

