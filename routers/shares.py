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
        raise HTTPException(status_code=400, detail="Invalid share amount")

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="buyer")

    # TODO: Replace with your actual share-buying logic
    # For now, just returning net amount after fee
    return {
        "message": "Shares purchased",
        "original_amount": amount,
        "fee": fee,
        "net_purchase": net_amount
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
        raise HTTPException(status_code=400, detail="Invalid share amount")

    net_amount, fee = apply_share_trade_fee(db, current_user, amount, role="seller")

    # TODO: Replace with your actual share-selling logic
    # For now, just returning net amount after fee
    return {
        "message": "Shares sold",
        "original_amount": amount,
        "fee": fee,
        "net_received": net_amount,
        "new_cumulative_sales": float(current_user.cumulative_sales)
                                 }
