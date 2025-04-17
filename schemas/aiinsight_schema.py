from pydantic import BaseModel

class AIInsightCreate(BaseModel):
    user_id: int
    query: str
    result: str

    model_config = {"from_attributes": True}


class AIInsightOut(BaseModel):
    id: int
    user_id: int
    query: str
    result: str
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
