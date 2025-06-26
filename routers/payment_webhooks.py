# File: routers/payment_webhooks.py

from fastapi import APIRouter, Request, HTTPException
from tortoise.transactions import in_transaction
from decimal import Decimal
from models.user import User
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarnings
from models.admin_wallet_log import AdminWalletLog
from utils.admin_wallet_logger import log_admin_wallet_activity

router = APIRouter(prefix="/webhooks", tags=["Payment Webhooks"])

# ─────────── PAYSTACK ───────────
@router.post("/paystack")
async def handle_paystack_webhook(request: Request):
    data = await request.json()
    event = data.get("event")
    payload = data.get("data", {})

    if event != "charge.success":
        return {"status": "ignored"}

    reference = payload.get("reference")
    email = payload.get("customer", {}).get("email")
    amount = Decimal(payload.get("amount", 0)) / 100  # Paystack sends kobo

    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    async with in_transaction():
        wallet, _ = await Wallet.get_or_create(user=user, defaults={"balance": 0})
        fee = Decimal("0.01") * amount
        net_amount = amount - fee

        wallet.balance += net_amount
        await wallet.save()

        await WalletTransaction.create(
            wallet=wallet,
            user=user,
            amount=net_amount,
            transaction_type="fund",
            description=f"Funded via Paystack (ref: {reference})"
        )

        admin_wallet = await AdminWallet.first()
        if not admin_wallet:
            admin_wallet = await AdminWallet.create(balance=0)

        admin_wallet.balance += fee
        await admin_wallet.save()

        await PlatformEarnings.create(user=user, source="paystack", amount=fee)

        await log_admin_wallet_activity(
            amount=fee,
            action="fee_credit",
            description=f"Paystack funding fee from user {user.id}",
            triggered_by=user
        )

    return {"status": "success"}