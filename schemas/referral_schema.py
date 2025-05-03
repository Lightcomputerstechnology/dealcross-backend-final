from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ───── User-Side Referrals ─────
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


# ───── Admin: Referral Reward Record ─────
class ReferralRewardOut(BaseModel):
    id: int
    inviter_id: int
    invitee_id: int
    reward_amount: float
    event: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ───── Admin: Manual Credit Input ─────
class ReferralManualCredit(BaseModel):
    inviter_id: int
    invitee_id: int
    amount: float
    event: Optional[str] = "manual_credit"