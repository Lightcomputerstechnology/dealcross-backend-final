from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models import User
from models.fraud import FraudAlert  # ✅ Added for fraud alerts
from utils.fee_calculator import apply_share_trade_fee

router = APIRouter(prefix="/shares", tags=["Share Trading"])

# === Fraud alert utility ===
def trigger_fraud_alert(db: Session, user_id: int, alert_type: str, description: str):
    alert = FraudAlert(user_id=user_id, alert_type=alert_type, description=description)
    db.add(alert)
    db.commit()

# === Get Available Shares ===
@router.get("/", summary="List available shares for trading")
def list_shares():
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
def buy_shares(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="buyer")
    fee_rate = "2%" if current_user.role.value == "basic" else "1.5%"

    # === Fraud detection: large share buy ===
    if amount >= 10000:
        trigger_fraud_alert(db, current_user.id, "large_share_buy", f"User purchased shares worth ${amount}.")

    return {
        "message": "Shares purchased successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "user_tier": current_user.role.value,
            "net_purchase": net_amount
        }
    }

# === Sell Shares ===
@router.post("/sell", summary="Sell shares with seller fee applied")
def sell_shares(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="seller")
    fee_rate = "1%" if current_user.role.value == "basic" else "0.75%"
    if current_user.cumulative_sales < 1000:
        fee_rate = "0%"

    # === Fraud detection: large share sell ===
    if amount >= 10000:
        trigger_fraud_alert(db, current_user.id, "large_share_sell", f"User sold shares worth ${amount}.")

    return {
        "message": "Shares sold successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "user_tier": current_user.role.value,
            "net_received": net_amount,
            "new_cumulative_sales": float(current_user.cumulative_sales)
        }
    }

# === Get user cumulative sales total ===
@router.get("/my-cumulative-sales", summary="View your cumulative share sales")
def get_my_cumulative_sales(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    progress = min(100, (current_user.cumulative_sales / 1000) * 100)
    return {
        "user_id": current_user.id,
        "cumulative_sales": float(current_user.cumulative_sales),
        "seller_fee_threshold": 1000.00,
        "fee_applies": current_user.cumulative_sales >= 1000,
        "progress_percent": round(progress, 2)
    }