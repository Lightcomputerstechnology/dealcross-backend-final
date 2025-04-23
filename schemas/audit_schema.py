from pydantic import BaseModel
from datetime import datetime

class AuditLogOut(BaseModel):
    id: int
    action: str
    performed_by: str
    timestamp: datetime
    details: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2 style
