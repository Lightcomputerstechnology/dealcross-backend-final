# File: routers/share.py

from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user
from models.user import User
from models.fraudalert import FraudAlert
from utils.fee_calculator import apply_share_trade_fee
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from models.admin_wallet import AdminWallet
from models.platform_earnings import PlatformEarning

router = APIRouter(prefix="/shares", tags=["Share Trading"])

# === Fraud alert utility ===
async def trigger_fraud_alert(user: User, alert_type: str, description: str):
    await FraudAlert.create(user=user, alert_type=alert_type, description=description)

# === Get Available Shares ===
@router.get("/", summary="List available shares for trading")
async def list_shares():
    return [
        {"name": "Bitcoin (BTC)", "symbol": "BTC", "price": 42000, "change": "+2.5%"},
        {"name": "Ethereum (ETH)", "symbol": "ETH", "price": 2600, "change": "-1.2%"},
        {"name": "Apple Inc. (AAPL)", "symbol": "AAPL", "price": 175, "change": "+0.8%"},
        {"name": "Tesla Inc. (TSLA)", "symbol": "TSLA", "price": 690, "change": "-0.3%"},
        {"name": "Google (GOOG)", "symbol": "GOOG", "price": 2950, "change": "+1.5%"},
        {"name": "Microsoft (MSFT)", "symbol": "MSFT", "price": 315, "change": "+0.9%"},
        {"name": "Amazon (AMZN)", "symbol": "AMZN", "price": 3280, "change": "-1.1%"},
        {"name": "Solana (SOL)", "symbol": "SOL", "price": 120, "change": "+5.3%"},
        {"name": "Meta Platforms (META)", "symbol": "META", "price": 250, "change": "+0.4%"}
    ]

# === Buy Shares ===
@router.post("/buy", summary="Buy shares with fee applied")
async def buy_shares(amount: float, current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = await apply_share_trade_fee(current_user, amount, role="buyer")
    wallet = await Wallet.get(user=current_user)
    total_deduction = amount + fee

    if wallet.balance < total_deduction:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

    wallet.balance -= total_deduction
    await wallet.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=amount,
        transaction_type="share_buy",
        description=f"Bought shares worth {amount} (fee: {fee})"
    )

    admin_wallet = await AdminWallet.first()
    if not admin_wallet:
        admin_wallet = await AdminWallet.create(balance=0)
    admin_wallet.balance += fee
    await admin_wallet.save()

    await PlatformEarning.create(
        user=current_user,
        source="share_buy",
        amount=fee
    )

    return {
        "message": "Shares purchased successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
            "fee_rate": "2%" if current_user.role.value == "user" else "1.5%",
            "net_purchase": net_amount
        }
    }

# === Sell Shares ===
@router.post("/sell", summary="Sell shares with seller fee applied")
async def sell_shares(amount: float, current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = await apply_share_trade_fee(current_user, amount, role="seller")
    wallet = await Wallet.get(user=current_user)
    wallet.balance += net_amount
    await wallet.save()

    current_user.cumulative_sales += amount
    await current_user.save()

    await WalletTransaction.create(
        wallet=wallet,
        user=current_user,
        amount=net_amount,
        transaction_type="share_sell",
        description=f"Sold shares worth {amount} (fee: {fee})"
    )

    if fee > 0:
        admin_wallet = await AdminWallet.first()
        if not admin_wallet:
            admin_wallet = await AdminWallet.create(balance=0)
        admin_wallet.balance += fee
        await admin_wallet.save()

        await PlatformEarning.create(
            user=current_user,
            source="share_sell",
            amount=fee
        )

    return {
        "message": "Shares sold successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
            "fee_rate": "0%" if current_user.cumulative_sales < 1000 else ("1%" if current_user.role.value == "user" else "0.7%"),
            "net_received": net_amount,
            "new_cumulative_sales": float(current_user.cumulative_sales)
        }
    }

# === Get user cumulative sales total ===
@router.get("/my-cumulative-sales", summary="View your cumulative share sales")
async def get_my_cumulative_sales(current_user: User = Depends(get_current_user)):
    progress = min(100, (current_user.cumulative_sales / 1000) * 100)
    return {
        "user_id": current_user.id,
        "cumulative_sales": float(current_user.cumulative_sales),
        "seller_fee_threshold": 1000.00,
        "fee_applies": current_user.cumulative_sales >= 1000,
        "progress_percent": round(progress, 2)
        }
    
