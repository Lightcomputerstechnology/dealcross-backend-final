# File: routers/wallet.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/fund")
def fund_wallet(amount: float = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    current_user.wallet_balance += amount
    db.commit()
    db.refresh(current_user)
    return {"message": "Wallet funded", "new_balance": current_user.wallet_balance}

@router.get("/balance")
def get_wallet_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"balance": current_user.wallet_balance}
