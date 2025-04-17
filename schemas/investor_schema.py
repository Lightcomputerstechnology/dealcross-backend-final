from pydantic import BaseModel
from typing import Optional


class InvestorCreate(BaseModel):
    user_id: int
    company_name: str
    pitch_deck_url: Optional[str] = None
    interest_area: Optional[str] = None

    model_config = {"from_attributes": True}


class InvestorOut(BaseModel):
    id: int
    user_id: int
    company_name: str
    pitch_deck_url: Optional[str]
    interest_area: Optional[str]
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
