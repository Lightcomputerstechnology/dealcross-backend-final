from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.deal import Deal, DealStatus
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from schemas.deal import DealCreate, DealOut
from models.user import User

router = APIRouter(prefix="/deals", tags=["Deals"])

# ─────────── CREATE DEAL ───────────
@router.post("/", response_model=DealOut)
def create_deal(deal_in: DealCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id == deal_in.counterparty_id:
        raise HTTPException(status_code=400, detail="Cannot create a deal with yourself.")

    new_deal = Deal(
        title=deal_in.title,
        amount=deal_in.amount,
        description=deal_in.description,
        public_deal=deal_in.public_deal,
        creator_id=current_user.id,
        counterparty_id=deal_in.counterparty_id
    )
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal

# ─────────── FUND DEAL ───────────
@router.post("/{deal_id}/fund")
def fund_deal(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.creator_id == current_user.id).first()
    if not deal or deal.status != DealStatus.pending:
        raise HTTPException(status_code=400, detail="Deal not found or cannot be funded.")

    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if wallet.balance < deal.amount:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

    wallet.balance -= deal.amount
    deal.status = DealStatus.active

    transaction = WalletTransaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        amount=deal.amount,
        transaction_type="escrow_fund",
        description=f"Funded Deal {deal.id}"
    )
    db.add(transaction)
    db.commit()
    return {"message": "Deal funded successfully."}

# ─────────── DELIVER DEAL ───────────
@router.post("/{deal_id}/deliver")
def mark_delivered(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.counterparty_id == current_user.id).first()
    if not deal or deal.status != DealStatus.active:
        raise HTTPException(status_code=400, detail="Deal not found or cannot be marked delivered.")

    deal.status = DealStatus.completed  # Can adjust to intermediate 'delivered' state
    db.commit()
    return {"message": "Deal marked as delivered."}

# ─────────── RELEASE FUNDS ───────────
@router.post("/{deal_id}/release")
def release_funds(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.creator_id == current_user.id).first()
    if not deal or deal.status != DealStatus.completed:
        raise HTTPException(status_code=400, detail="Deal not ready for release.")

    seller_wallet = db.query(Wallet).filter(Wallet.user_id == deal.counterparty_id).first()
    seller_wallet.balance += deal.amount

    transaction = WalletTransaction(
        wallet_id=seller_wallet.id,
        user_id=deal.counterparty_id,
        amount=deal.amount,
        transaction_type="escrow_release",
        description=f"Released funds for Deal {deal.id}"
    )
    db.add(transaction)
    db.commit()
    return {"message": "Funds released to seller."}

# ─────────── RAISE DISPUTE ───────────
@router.post("/{deal_id}/dispute")
def raise_dispute(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deal = db.query(Deal).filter(
        Deal.id == deal_id,
        ((Deal.creator_id == current_user.id) | (Deal.counterparty_id == current_user.id))
    ).first()
    if not deal or deal.status not in [DealStatus.active, DealStatus.completed]:
        raise HTTPException(status_code=400, detail="Cannot dispute this deal.")

    deal.status = DealStatus.disputed
    db.commit()
    return {"message": "Deal marked as disputed."}