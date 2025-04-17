from pydantic import BaseModel
from datetime import datetime

class AIInsightBase(BaseModel):
    content: str

class AIInsightCreate(AIInsightBase):
    pass

class AIInsightOut(AIInsightBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
