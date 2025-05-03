# File: routers/subscription.py

from fastapi import APIRouter, HTTPException, Depends, Request
from core.security import get_current_user
from pydantic import BaseModel
from tortoise.transactions import in_transaction

router = APIRouter(prefix="/subscription", tags=["Subscription"])

# ─────────── Payload Schema ───────────
class SubscriptionRequest(BaseModel):
    plan: str
    payment_method: str

# ─────────── Valid Plans ───────────
VALID_PLANS = {
    "basic": 0,
    "pro": 10000,
    "business": 25000
}

# ─────────── Endpoint ───────────
@router.post("/upgrade")
async def upgrade_user_plan(
    payload: SubscriptionRequest,
    request: Request,
    current_user=Depends(get_current_user)
):
    if payload.plan not in VALID_PLANS:
        raise HTTPException(status_code=400, detail="Invalid subscription plan selected.")

    payment_success = True  # Replace with real payment logic

    if not payment_success:
        raise HTTPException(status_code=402, detail="Payment failed.")

    # Update user's subscription_plan safely
    async with in_transaction():
        current_user.subscription_plan = payload.plan
        await current_user.save()

    return {
        "message": f"Subscription upgraded to {payload.plan} successfully.",
        "amount_charged": VALID_PLANS[payload.plan],
        "user": current_user.username
    }
