# File: schemas/fraud.py

from datetime import datetime
from pydantic import BaseModel


class FraudAlertOut(BaseModel):
    id: int
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
