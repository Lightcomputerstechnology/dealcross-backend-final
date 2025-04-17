from pydantic import BaseModel
from typing import Optional


class ChatMessageCreate(BaseModel):
    deal_id: int
    sender_id: int
    message: str

    model_config = {"from_attributes": True}


class ChatMessageOut(BaseModel):
    id: int
    deal_id: int
    sender_id: int
    message: str
    timestamp: str  # ISO format

    model_config = {"from_attributes": True}
