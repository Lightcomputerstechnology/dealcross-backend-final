# File: routers/admin_referral.py

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist
from typing import List
from models.user import User
from models.referral_reward import ReferralReward
from core.security import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/admin/referrals", tags=["Admin Referral Management"])

# ─────────── Schemas ───────────
class ReferralRewardOut(BaseModel):
    id: int
    referrer_id: int
    referred_id: int
    source: str
    amount: float
    approved_by_admin: bool
    timestamp: datetime

    model_config = {"from_attributes": True}

# ─────────── Get All Referral Rewards ───────────
@router.get("/", response_model=List[ReferralRewardOut])
async def list_referral_rewards(current_user: User = Depends(get_current_user)):
    if not current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only access")
    
    rewards = await ReferralReward.all().order_by("-timestamp")
    return [ReferralRewardOut.model_validate(r) for r in rewards]

# ─────────── Approve Referral Reward ───────────
@router.put("/approve/{reward_id}", summary="Approve a pending referral reward")
async def approve_referral_reward(reward_id: int, current_user: User = Depends(get_current_user)):
    if not current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only access")

    try:
        reward = await ReferralReward.get(id=reward_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Referral reward not found")

    reward.approved_by_admin = True
    await reward.save()
    return {"message": "Referral reward approved."}

# ─────────── Unapprove Referral Reward ───────────
@router.put("/unapprove/{reward_id}", summary="Revoke admin approval")
async def unapprove_referral_reward(reward_id: int, current_user: User = Depends(get_current_user)):
    if not current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only access")

    try:
        reward = await ReferralReward.get(id=reward_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Referral reward not found")

    reward.approved_by_admin = False
    await reward.save()
    return {"message": "Referral reward unapproved."}