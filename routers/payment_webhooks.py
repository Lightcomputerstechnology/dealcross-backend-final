# File: routers/payment_webhooks.py

from fastapi import APIRouter, Request, HTTPException
from decimal import Decimal
from tortoise.transactions import in_transaction
from tortoise.expressions import Q

# MODELS
from models.user import User
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarnings

# UTILS
from utils.admin_wallet_logger import log_admin_wallet_activity

router = APIRouter(prefix="/webhooks", tags=["Payment Webhooks"])

# ─────────── PAYSTACK ───────────
@router.post("/paystack")
async def handle_paystack_webhook(request: Request):
    payload = await request.json()
    event = payload.get("event")

    if event != "charge.success":
        return {"message": "Ignored non-charge event"}

    data = payload.get("data", {})
    email = data.get("customer", {}).get("email")
    amount_raw = data.get("amount")  # Paystack sends in kobo
    reference = data.get("reference")

    if not email or not amount_raw or not reference:
        raise HTTPException(status_code=400, detail="Invalid payload")

    async with in_transaction():
        user = await User.get_or_none(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Prevent duplicate
        exists = await WalletTransaction.get_or_none(description__icontains=reference)
        if exists:
            return {"message": "Duplicate payment"}

        wallet, _ = await Wallet.get_or_create(user=user, defaults={"balance": 0})
        amount = Decimal(amount_raw) / 100  # Convert kobo to naira

        wallet.balance += amount
        await wallet.save()

        await WalletTransaction.create(
            wallet=wallet,
            user=user,
            amount=amount,
            transaction_type="fund",
            description=f"Paystack top-up: {reference}"
        )

        admin_wallet = await AdminWallet.first()
        if not admin_wallet:
            admin_wallet = await AdminWallet.create(balance=0)

        fee = Decimal("0.00")
        admin_wallet.balance += fee
        await admin_wallet.save()

        await PlatformEarnings.create(user=user, source="paystack", amount=fee)
        await log_admin_wallet_activity(
            amount=fee,
            action="paystack_fee",
            description=f"Fee from Paystack {reference}",
            triggered_by=user
        )

    return {"message": "Paystack webhook processed"}


# ─────────── FLUTTERWAVE ───────────
@router.post("/flutterwave")
async def handle_flutterwave_webhook(request: Request):
    payload = await request.json()
    data = payload.get("data", {})
    status = data.get("status")
    tx_ref = data.get("tx_ref")
    amount = data.get("amount")
    email = data.get("customer", {}).get("email")

    if status != "successful":
        return {"message": "Ignored non-successful transaction"}

    if not email or not amount or not tx_ref:
        raise HTTPException(status_code=400, detail="Invalid Flutterwave payload")

    async with in_transaction():
        user = await User.get_or_none(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        exists = await WalletTransaction.get_or_none(description__icontains=tx_ref)
        if exists:
            return {"message": "Duplicate Flutterwave payment"}

        wallet, _ = await Wallet.get_or_create(user=user, defaults={"balance": 0})
        amount = Decimal(str(amount))

        wallet.balance += amount
        await wallet.save()

        await WalletTransaction.create(
            wallet=wallet,
            user=user,
            amount=amount,
            transaction_type="fund",
            description=f"Flutterwave top-up: {tx_ref}"
        )

        fee = Decimal("0.00")
        admin_wallet = await AdminWallet.first()
        if not admin_wallet:
            admin_wallet = await AdminWallet.create(balance=0)

        admin_wallet.balance += fee
        await admin_wallet.save()

        await PlatformEarnings.create(user=user, source="flutterwave", amount=fee)
        await log_admin_wallet_activity(
            amount=fee,
            action="flutterwave_fee",
            description=f"Fee from Flutterwave {tx_ref}",
            triggered_by=user
        )

    return {"message": "Flutterwave webhook processed"}


# ─────────── NOWPAYMENTS ───────────
@router.post("/nowpayments")
async def handle_nowpayments_webhook(request: Request):
    payload = await request.json()
    payment_status = payload.get("payment_status")
    order_id = payload.get("order_id")
    pay_address = payload.get("pay_address")
    pay_amount = payload.get("pay_amount")

    if payment_status != "finished":
        return {"message": "Payment not completed"}

    user = await User.get_or_none(id=order_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    exists = await WalletTransaction.get_or_none(description__icontains=pay_address)
    if exists:
        return {"message": "Duplicate crypto payment"}

    wallet, _ = await Wallet.get_or_create(user=user, defaults={"balance": 0})
    amount = Decimal(str(pay_amount))

    wallet.balance += amount
    await wallet.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=user,
        amount=amount,
        transaction_type="fund",
        description=f"Crypto funding to {pay_address}"
    )

    fee = Decimal("0.00")
    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)

    admin_wallet.balance += fee
    await admin_wallet.save()

    await PlatformEarnings.create(user=user, source="crypto", amount=fee)
    await log_admin_wallet_activity(
        amount=fee,
        action="crypto_fee",
        description=f"Fee from crypto funding {pay_address}",
        triggered_by=user
    )

    return {"message": "NOWPayments webhook processed"}