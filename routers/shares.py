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

    - **amount**: Amount of shares to buy.
    - **fee**: Deducted based on user tier.
    - **Returns**: Net amount of shares purchased after fee.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid share amount")

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="buyer")

    return {
        "message": "Shares purchased successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
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

    - **amount**: Amount of shares to sell.
    - **fee**: Deducted based on user tier and cumulative sales.
    - **Returns**: Net amount received and updated cumulative sales.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid share amount")

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="seller")

    return {
        "message": "Shares sold successfully",
        "data": {
            "original_amount": amount,
            "fee": fee,
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

    - Helps track when seller fees begin (after $1,000 threshold).
    """
    return {
        "user_id": current_user.id,
        "cumulative_sales": float(current_user.cumulative_sales),
        "seller_fee_threshold": 1000.00,
        "fee_applies": current_user.cumulative_sales >= 1000
    }
