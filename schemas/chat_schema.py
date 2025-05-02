# File: schemas/chat_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessageCreate(BaseModel):
    receiver_id: int
    content: str
    deal_id: Optional[int] = None


class ChatMessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    deal_id: Optional[int]
    content: str
    is_read: bool
    timestamp: datetime

    model_config = {"from_attributes": True}