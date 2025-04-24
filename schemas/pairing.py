from pydantic import BaseModel, EmailStr
from enum import Enum

class PairingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"

class PairRequest(BaseModel):
    counterparty_email: EmailStr

class PairOut(BaseModel):
    id: int
    creator_id: int
    counterparty_id: int
    status: PairingStatus

    model_config = {"from_attributes": True}