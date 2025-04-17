from pydantic import BaseModel
from typing import Optional


class FeedbackCreate(BaseModel):
    user_id: int
    rating: int  # from 1 to 5
    comment: Optional[str] = None

    model_config = {"from_attributes": True}


class FeedbackOut(BaseModel):
    id: int
    user_id: int
    rating: int
    comment: Optional[str]
    submitted_at: str  # ISO format

    model_config = {"from_attributes": True}
