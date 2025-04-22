# File: routers/wallet.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import get_current_user
from models.wallet import Wallet
from models.user import User
from models.wallet_transaction import WalletTransaction  # ✅ For transaction logs
from schemas.wallet import WalletCreate, WalletOut
from schemas.wallet_transaction import WalletTransactionOut  # ✅ Transaction schema
from typing import List

router = APIRouter(prefix="/wallet", tags=["Wallet Management"])  # ✅ Tag added

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Get current user's wallet ===
@router.get("/my-wallet", response_model=WalletOut, summary="Retrieve the current user's wallet")
def get_my_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the wallet details of the currently logged-in user.

    - **Returns**: Wallet balance and user ID.
    """
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

# === Fund wallet with transaction logging ===
@router.post("/fund", response_model=WalletOut, summary="Fund the user's wallet")
def fund_wallet(payload: WalletCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Adds funds to the logged-in user's wallet.

    - **amount**: The amount to fund the wallet with.
    - **Logs**: Transaction recorded in the transaction history.
    """
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=payload.amount)
        db.add(wallet)
    else:
        wallet.balance += payload.amount

    # ✅ Log transaction
    db.add(WalletTransaction(
        user_id=current_user.id,
        amount=payload.amount,
        transaction_type="fund",
        description="Wallet funded"
    ))

    db.commit()
    db.refresh(wallet)
    return wallet

# === Get wallet transaction history ===
@router.get("/transactions", response_model=List[WalletTransactionOut], summary="View wallet transaction history")
def get_wallet_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the transaction history of the logged-in user's wallet.

    - **Returns**: List of all wallet transactions, ordered by most recent.
    """
    transactions = db.query(WalletTransaction).filter(
        WalletTransaction.user_id == current_user.id
    ).order_by(WalletTransaction.timestamp.desc()).all()
    return transactions
