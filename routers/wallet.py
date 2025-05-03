# File: routers/wallet.py
from decimal import Decimal
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user

# MODELS
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.fee_transaction import FeeTransaction           # (still used in /my-wallet)
from models.fraud import FraudAlert
from models.user import User
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarning        # NEW import

# SERVICES / UTILS
from services.fee_logic import calculate_fee                # NEW import

# SCHEMAS
from schemas.wallet import WalletOut, FundWallet, TransactionOut

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

# ─────────── FRAUD ALERT HELPER ───────────
async def trigger_fraud_alert(user: User, alert_type: str, description: str):
    await FraudAlert.create(user=user, alert_type=alert_type, description=description)

# ─────────── GET WALLET SUMMARY ───────────
@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions")
async def get_my_wallet_summary(current_user: User = Depends(get_current_user)):
    ...
    # (unchanged code for summary / fraud detection)
    ...

# ─────────── FUND WALLET  (UPDATED) ───────────
@router.post("/fund", summary="Fund user's wallet (applies funding fee)")
async def fund_wallet(fund: FundWallet, current_user: User = Depends(get_current_user)):
    # 1. Calculate fee
    base_amount = Decimal(fund.amount)
    fee = Decimal(calculate_fee(current_user, "funding", float(base_amount)))
    net_amount = base_amount - fee

    # 2. Update / create user's wallet
    wallet, _ = await Wallet.get_or_create(user=current_user, defaults={"balance": 0})
    wallet.balance += net_amount
    await wallet.save()

    # 3. Log wallet transaction
    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=net_amount,
        transaction_type="fund",
        description=f"Wallet funded (fee: {fee})"
    )

    # 4. Update Admin Wallet
    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)
    admin_wallet.balance += fee
    await admin_wallet.save()

    # 5. Log platform earnings
    await PlatformEarning.create(
        user=current_user,
        source="funding",
        amount=fee
    )

    return {
        "message": f"Wallet funded with {net_amount} (fee {fee})",
        "net_amount": float(net_amount),
        "fee": float(fee)
    }

# ─────────── GET ALL TRANSACTIONS ───────────
@router.get("/transactions", summary="Retrieve all wallet transactions for the current user")
async def get_all_transactions(current_user: User = Depends(get_current_user)):
    ...
