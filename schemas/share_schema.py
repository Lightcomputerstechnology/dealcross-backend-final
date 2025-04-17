from pydantic import BaseModel
from typing import Optional


class ShareCreate(BaseModel):
    symbol: str
    company_name: str
    price: float
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class ShareOut(BaseModel):
    id: int
    symbol: str
    company_name: str
    price: float
    description: Optional[str] = None

    model_config = {"from_attributes": True}
