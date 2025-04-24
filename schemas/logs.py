from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FraudAlertCreate(BaseModel):
    deal_id: int
    reason: str

class FraudAlertOut(BaseModel):
    id: int
    deal_id: int
    reporter_id: int
    reason: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}

class AuditLogOut(BaseModel):
    id: int
    action: str
    performed_by: int
    timestamp: datetime

    model_config = {"from_attributes": True}