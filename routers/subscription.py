# File: routers/subscription.py

from fastapi import APIRouter, HTTPException, Depends, Request
from models.user import User
from core.security import get_current_user
from pydantic import BaseModel
from tortoise.transactions import in_transaction

router = APIRouter(prefix="/subscription", tags=["Subscription"])

# Payload schema
class SubscriptionRequest(BaseModel):
    plan: str
    payment_method: str

# Valid plans
VALID_PLANS = {
    "basic": 0,
    "pro": 10000,        # In Naira
    "business": 25000
}

# Endpoint to upgrade user's subscription
@router.post("/upgrade")
async def upgrade_user_plan(
    payload: SubscriptionRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if payload.plan not in VALID_PLANS:
        raise HTTPException(status_code=400, detail="Invalid subscription plan selected.")

    # Simulated payment success (replace with actual integration)
    payment_success = True

    if not payment_success:
        raise HTTPException(status_code=402, detail="Payment processing failed.")

    # Update user subscription
    async with in_transaction():
        current_user.subscription_plan = payload.plan
        await current_user.save()

    return {
        "message": f"Subscription upgraded to {payload.plan} plan successfully.",
        "amount_charged": VALID_PLANS[payload.plan],
        "user": current_user.username
}
