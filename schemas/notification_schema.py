from pydantic import BaseModel
from typing import Optional


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: Optional[bool] = False

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
