# File: models/config.py

from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
