# File: models/settings.py

from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class AppSettings(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String, unique=True, nullable=False)
    setting_value = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
