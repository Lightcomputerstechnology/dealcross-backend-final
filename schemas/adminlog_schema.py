from pydantic import BaseModel
from typing import Optional


class AdminLogCreate(BaseModel):
    admin_id: int
    action: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class AdminLogOut(BaseModel):
    id: int
    admin_id: int
    action: str
    description: Optional[str]
    timestamp: str  # ISO format

    model_config = {"from_attributes": True}
