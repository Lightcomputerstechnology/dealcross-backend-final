# File: routers/subscription.py

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from tortoise.transactions import in_transaction

from core.security import get_current_user  # returns JWT claims (Supabase-aware)
from models.user import User  # local user model

router = APIRouter(prefix="/subscription", tags=["Subscription"])


class SubscriptionRequest(BaseModel):
    plan: str
    payment_method: str


VALID_PLANS = {
    "basic": 0,
    "pro": 10000,
    "business": 25000
}


# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


@router.post("/upgrade")
async def upgrade_user_plan(
    payload: SubscriptionRequest,
    request: Request,
    current_user: User = Depends(resolve_db_user),
):
    if payload.plan not in VALID_PLANS:
        raise HTTPException(status_code=400, detail="Invalid subscription plan selected.")

    # TODO: plug real payment check here based on payload.payment_method
    payment_success = True

    if not payment_success:
        raise HTTPException(status_code=402, detail="Payment failed.")

    async with in_transaction():
        current_user.subscription_plan = payload.plan
        await current_user.save()

    return {
        "message": f"Subscription upgraded to {payload.plan} successfully.",
        "amount_charged": VALID_PLANS[payload.plan],
        "user": getattr(current_user, "username", current_user.email)
                            }
