# File: src/models/share.py

from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Share(Base):
    __tablename__ = "shares"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    change = Column(String, nullable=True)