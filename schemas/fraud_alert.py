# File: src/schemas/fraud_alert.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FraudAlertCreate(BaseModel):
    alert_type: str
    description: str

class FraudAlertOut(BaseModel):
    id: int
    user_id: int
    alert_type: str
    description: str
    timestamp: datetime

    model_config = {"from_attributes": True}