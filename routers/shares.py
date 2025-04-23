from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from utils.fee_calculator import apply_share_trade_fee

router = APIRouter(prefix="/shares", tags=["Share Trading"])

# === Buy Shares ===
@router.post("/buy", summary="Buy shares with fee applied")
def buy_shares(
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Buys shares by deducting buyer fee and crediting admin wallet.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="buyer")
    fee_rate = "2%" if current_user.role.value == "basic" else "1.5%"

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
def sell_shares(
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sells shares by deducting seller fee and updating cumulative sales.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail={"error": True, "message": "Invalid share amount."})

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="seller")
    fee_rate = "1%" if current_user.role.value == "basic" else "0.75%"
    if current_user.cumulative_sales < 1000:
        fee_rate = "0%"  # No fee under $1,000

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
def get_my_cumulative_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the total cumulative sales made by the user.
    """
    progress = min(100, (current_user.cumulative_sales / 1000) * 100)
    return {
        "user_id": current_user.id,
        "cumulative_sales": float(current_user.cumulative_sales),
        "seller_fee_threshold": 1000.00,
        "fee_applies": current_user.cumulative_sales >= 1000,
        "progress_percent": round(progress, 2)
    }
