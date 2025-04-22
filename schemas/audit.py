# File: schemas/audit.py

from pydantic import BaseModel
from datetime import datetime

class AuditLogOut(BaseModel):
    id: int
    admin_id: int
    action: str
    target_type: str
    target_id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
