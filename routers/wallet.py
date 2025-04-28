from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from core.security import get_current_user
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.fee_transaction import FeeTransaction
from models.fraud import FraudAlert
from models.user import User
from schemas.wallet import WalletOut, FundWallet, TransactionOut

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])

# ─────────── FRAUD ALERT HELPER ───────────

async def trigger_fraud_alert(user: User, alert_type: str, description: str):
    await FraudAlert.create(user=user, alert_type=alert_type, description=description)

# ─────────── GET WALLET SUMMARY ───────────

@router.get("/my-wallet", summary="Retrieve user's wallet balance and recent transactions")
async def get_my_wallet_summary(current_user: User = Depends(get_current_user)):
    wallet = await Wallet.get_or_none(user=current_user)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found.")

    # Total funded
    funded_agg = await WalletTransaction.filter(
        user=current_user,
        transaction_type="fund"
    ).annotate(sum_amount=WalletTransaction.amount.sum())

    total_funded = funded_agg[0].sum_amount if funded_agg else 0.00

    # Total spent
    spent_agg = await WalletTransaction.filter(
        user=current_user,
        transaction_type="spend"
    ).annotate(sum_amount=WalletTransaction.amount.sum())

    total_spent = spent_agg[0].sum_amount if spent_agg else 0.00

    # Total fees paid
    fees_agg = await FeeTransaction.filter(
        user=current_user
    ).annotate(sum_amount=FeeTransaction.amount.sum())

    total_fees_paid = fees_agg[0].sum_amount if fees_agg else 0.00

    # Recent Transactions
    recent_transactions = await WalletTransaction.filter(
        user=current_user
    ).order_by("-timestamp").limit(5)

    # Fraud detection: Frequent Funding within 10 min
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_fundings = await WalletTransaction.filter(
        user=current_user,
        transaction_type="fund",
        timestamp__gte=ten_minutes_ago
    ).count()

    if recent_fundings >= 5:
        await trigger_fraud_alert(current_user, "frequent_funding", f"User funded {recent_fundings} times within 10 minutes.")

    return {
        "wallet": WalletOut.model_validate(wallet),
        "summary": {
            "total_funded": float(total_funded or 0.00),
            "total_spent": float(total_spent or 0.00),
            "total_fees_paid": float(total_fees_paid or 0.00)
        },
        "recent_transactions": [TransactionOut.model_validate(tx) for tx in recent_transactions]
    }

# ─────────── FUND WALLET ───────────

@router.post("/fund", summary="Fund user's wallet")
async def fund_wallet(fund: FundWallet, current_user: User = Depends(get_current_user)):
    wallet, _ = await Wallet.get_or_create(user=current_user, defaults={"balance": 0.0})

    wallet.balance += fund.amount
    await wallet.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=fund.amount,
        transaction_type="fund",
        description="Wallet funding"
    )

    return {"message": f"Wallet funded with {fund.amount} USD"}

# ─────────── GET ALL TRANSACTIONS ───────────

@router.get("/transactions", summary="Retrieve all wallet transactions for the current user")
async def get_all_transactions(current_user: User = Depends(get_current_user)):
    transactions = await WalletTransaction.filter(user=current_user).order_by("-timestamp")
    return [TransactionOut.model_validate(tx) for tx in transactions]
