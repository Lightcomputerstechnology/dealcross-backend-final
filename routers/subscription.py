✅ File: routers/subscription.py

from fastapi import APIRouter, HTTPException, Depends, Request
from models.user import User
from core.security import get_current_user
from pydantic import BaseModel
from tortoise.transactions import in_transaction

router = APIRouter(prefix="/subscription", tags=["Subscription"])

# ─────────── Payload Schema ───────────
class SubscriptionRequest(BaseModel):
    plan: str
    payment_method: str

# ─────────── Available Plans ───────────
VALID_PLANS = {
    "basic": 0,
    "pro": 10000,         # In Naira or preferred currency
    "business": 25000
}

# ─────────── Endpoint: Upgrade Plan ───────────
@router.post("/upgrade")
async def upgrade_user_plan(
    payload: SubscriptionRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if payload.plan not in VALID_PLANS:
        raise HTTPException(status_code=400, detail="Invalid subscription plan selected.")

    # Payment logic (to integrate with Stripe, Paystack, etc.)
    # Mock success for now:
    payment_success = True

    if not payment_success:
        raise HTTPException(status_code=402, detail="Payment processing failed.")

    # Save upgrade status to user
    async with in_transaction():
        current_user.subscription_plan = payload.plan
        await current_user.save()

    return {
        "message": f"Subscription upgraded to {payload.plan} plan successfully.",
        "amount_charged": VALID_PLANS[payload.plan],
        "user": current_user.username
    }


---

✅ Required Addition to models/user.py (if not already included):

subscription_plan = fields.CharField(max_length=20, default="basic")
