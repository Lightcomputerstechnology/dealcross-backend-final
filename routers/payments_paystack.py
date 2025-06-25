# routers/payments_paystack.py

from fastapi import APIRouter, Request, HTTPException
import httpx, os
from models.user import User
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.platform_earnings import PlatformEarnings
from services.fee_logic import calculate_fee
from utils.admin_wallet_logger import log_admin_wallet_activity

router = APIRouter(prefix="/api/paystack", tags=["Payments"])

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


@router.post("/verify")
async def verify_paystack_payment(request: Request):
    body = await request.json()
    reference = body.get("reference")

    if not reference:
        raise HTTPException(status_code=400, detail="Missing reference")

    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers)

    data = res.json()
    if data["status"] != True:
        raise HTTPException(status_code=400, detail="Verification failed")

    payment = data["data"]
    email = payment["customer"]["email"]
    amount = float(payment["amount"]) / 100  # Convert from kobo to NGN

    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    fee = calculate_fee(user, "funding", amount)
    net_amount = amount - fee

    wallet, _ = await Wallet.get_or_create(user=user, defaults={"balance": 0})
    wallet.balance += net_amount
    await wallet.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=user,
        amount=net_amount,
        transaction_type="fund",
        description=f"Paystack funding (fee: ₦{fee})"
    )

    await PlatformEarnings.create(
        user=user,
        source="funding",
        amount=fee
    )

    await log_admin_wallet_activity(
        amount=fee,
        action="fee_credit",
        description=f"Paystack funding fee from {user.email}",
        triggered_by=user
    )

    return {
        "message": "Wallet funded successfully",
        "gross_amount": amount,
        "net_amount": net_amount,
        "fee": fee
    }
