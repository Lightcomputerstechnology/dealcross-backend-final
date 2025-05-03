# File: routers/admin_referrals.py

from fastapi import APIRouter, Depends, HTTPException
from models.referral_reward import ReferralReward
from models.user import User
from core.security import get_current_user
from schemas.referral_schema import ReferralRewardOut, ReferralManualCredit
from tortoise.expressions import Q

router = APIRouter(prefix="/admin/referrals", tags=["Admin Referral"])

# Admin guard
def require_admin(user: User):
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only.")
    return user

# ─────────── View All Referral Bonuses ───────────
@router.get("/rewards", response_model=list[ReferralRewardOut])
async def view_all_referral_rewards(current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    rewards = await ReferralReward.all().prefetch_related("inviter", "invitee").order_by("-created_at")
    return [await ReferralRewardOut.from_tortoise_orm(r) for r in rewards]

# ─────────── Manually Credit Referral Bonus ───────────
@router.post("/credit", summary="Manually credit a referral bonus")
async def credit_referral_bonus(
    data: ReferralManualCredit,
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    reward = await ReferralReward.create(
        inviter_id=data.inviter_id,
        invitee_id=data.invitee_id,
        reward_amount=data.amount,
        event=data.event or "manual_credit"
    )

    return {
        "message": f"Referral bonus of ${data.amount} credited manually.",
        "id": reward.id
    }