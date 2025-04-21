# File: schemas/fraud.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# === Fraud Alert Base ===
class FraudBase(BaseModel):
    message: str
    level: Optional[str] = "medium"  # e.g., "low", "medium", "high"

# === Output Schema ===
class FraudAlertOut(FraudBase):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
