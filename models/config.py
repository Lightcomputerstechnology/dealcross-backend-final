# File: models/config.py

from sqlalchemy import Column, Integer, String
from core.database import Base

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)   # e.g., 'fraud_threshold'
    value = Column(String, nullable=False)              # Stored as string (convert as needed)
