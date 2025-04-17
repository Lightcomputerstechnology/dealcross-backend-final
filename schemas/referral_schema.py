from pydantic import BaseModel


class ReferralCreate(BaseModel):
    referrer_id: int
    referee_email: str

    model_config = {"from_attributes": True}


class ReferralOut(BaseModel):
    id: int
    referrer_id: int
    referee_email: str
    status: str
    created_at: str  # ISO format

    model_config = {"from_attributes": True}
