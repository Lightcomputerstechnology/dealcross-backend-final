# File: src/schemas/fraud_alert.py

from pydantic import BaseModel
from datetime import datetime

class FraudAlertOut(BaseModel):
    id: int
    user_id: int
    alert_type: str
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True