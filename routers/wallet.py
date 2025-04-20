# File: routers/wallet.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import get_current_user
from models.wallet import Wallet
from models.user import User
from schemas.wallet import WalletCreate, WalletOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/my-wallet", response_model=WalletOut)
def get_my_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/fund", response_model=WalletOut)
def fund_wallet(payload: WalletCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=payload.amount)
        db.add(wallet)
    else:
        wallet.balance += payload.amount

    db.commit()
    db.refresh(wallet)
    return wallet
