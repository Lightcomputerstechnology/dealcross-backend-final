# File: routers/wallet.py

from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request

from core.security import get_current_user  # returns JWT claims (Supabase-aware)
from utils.admin_wallet_logger import log_admin_wallet_activity

# MODELS
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.fee_transaction import FeeTransaction
from models.fraud import FraudAlert
from models.user import User
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarnings
from models.admin_wallet_log import AdminWalletLog

# SCHEMAS
from schemas.wallet import WalletOut, FundWallet, TransactionOut

# SERVICES
from services.fee_logic import calculate_fee
from services.payment_gateways import (
    initiate_paystack_payment,
    initiate_flutterwave_payment,
    initiate_nowpayments_crypto,
)

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])


# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


# ─────────── FRAUD ALERT HELPER ───────────
async def trigger_fraud_alert(user: User, alert_type: str, description: str):
    await FraudAlert.create(user=user, alert_type=alert_type, description=description)


# ─────────── GET WALLET SUMMARY ───────────
@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions")
async def get_my_wallet_summary(current_user: User = Depends(resolve_db_user)):
    wallet = await Wallet.get_or_none(user=current_user)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found.")

    funded_total = await WalletTransaction.filter(user=current_user, transaction_type="fund").annotate(
        sum_amount=WalletTransaction.amount.sum()
    )
    total_funded = funded_total[0].sum_amount if funded_total else 0.00

    spent_total = await WalletTransaction.filter(user=current_user, transaction_type="spend").annotate(
        sum_amount=WalletTransaction.amount.sum()
    )
    total_spent = spent_total[0].sum_amount if spent_total else 0.00

    fees_total = await FeeTransaction.filter(user=current_user).annotate(
        sum_amount=FeeTransaction.amount.sum()
    )
    total_fees_paid = fees_total[0].sum_amount if fees_total else 0.00

    recent_transactions = await WalletTransaction.filter(user=current_user).order_by("-timestamp").limit(5)

    # Fraud Detection
    recent_fundings = await WalletTransaction.filter(
        user=current_user, transaction_type="fund",
        timestamp__gte=datetime.utcnow() - timedelta(minutes=10)
    ).count()

    if recent_fundings >= 5:
        await trigger_fraud_alert(current_user, "frequent_funding", f"{recent_fundings} fundings in 10 min")

    return {
        "wallet": WalletOut.model_validate(wallet),
        "summary": {
            "total_funded": float(total_funded or 0),
            "total_spent": float(total_spent or 0),
            "total_fees_paid": float(total_fees_paid or 0),
        },
        "recent_transactions": [TransactionOut.model_validate(tx) for tx in recent_transactions]
    }


# ─────────── FUND WALLET (INTERNAL LOGIC ONLY) ───────────
@router.post("/fund", summary="Fund user's wallet (fee applies)")
async def fund_wallet(fund: FundWallet, current_user: User = Depends(resolve_db_user)):
    base_amount = Decimal(fund.amount)
    fee = Decimal(calculate_fee(current_user, "funding", float(base_amount)))
    net_amount = base_amount - fee

    wallet, _ = await Wallet.get_or_create(user=current_user, defaults={"balance": 0})
    wallet.balance += net_amount
    await wallet.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=net_amount,
        transaction_type="fund",
        description=f"Wallet funded (fee: {fee})"
    )

    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)

    admin_wallet.balance += fee
    await admin_wallet.save()

    await PlatformEarnings.create(
        user=current_user,
        source="funding",
        amount=fee
    )

    await log_admin_wallet_activity(
        amount=fee,
        action="fee_credit",
        description=f"Funding fee from user {current_user.id}",
        triggered_by=current_user
    )

    return {
        "message": f"Wallet funded with {net_amount} (fee {fee})",
        "net_amount": float(net_amount),
        "fee": float(fee)
    }


# ─────────── GET ALL TRANSACTIONS ───────────
@router.get("/transactions", summary="Retrieve all wallet transactions for the current user")
async def get_all_transactions(current_user: User = Depends(resolve_db_user)):
    transactions = await WalletTransaction.filter(user=current_user).order_by("-timestamp")
    return [TransactionOut.model_validate(tx) for tx in transactions]


# ─────────── EXTERNAL FUNDING ROUTES ───────────

@router.post("/fund/card", summary="Fund wallet via Card (Paystack)")
async def fund_wallet_card(request: Request, amount: float, current_user: User = Depends(resolve_db_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount.")
    payment_url = await initiate_paystack_payment(current_user, amount)
    return {"payment_url": payment_url}


@router.post("/fund/bank", summary="Fund wallet via Bank Transfer (Flutterwave)")
async def fund_wallet_bank(request: Request, amount: float, current_user: User = Depends(resolve_db_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount.")
    payment_url = await initiate_flutterwave_payment(current_user, amount, payment_type="bank")
    return {"payment_url": payment_url}


@router.post("/fund/crypto", summary="Fund wallet via Crypto (NowPayments)")
async def fund_wallet_crypto(request: Request, amount: float, crypto: str, current_user: User = Depends(resolve_db_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount.")
    invoice_data = await initiate_nowpayments_crypto(current_user, amount, crypto)
    return invoice_data
