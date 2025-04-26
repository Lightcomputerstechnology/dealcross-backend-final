# File: src/routers/deals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.deal import Deal, DealStatus
from models.user import User
from models.wallet import Wallet
from models.wallet_transaction import WalletTransaction
from schemas.deal import DealCreate, DealOut

# Commented out notification imports until core.email_utils/send_email is wired up:
# from core.email_utils import send_email
# from utils.notifications import create_notification

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.post("/", response_model=DealOut, summary="Create a new deal")
def create_deal(
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DealOut:
    """
    Create a new deal with pending status.
    """
    new_deal = Deal(
        **deal.dict(),
        creator_id=current_user.id,
        status=DealStatus.pending
    )
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal


@router.post("/{deal_id}/fund", summary="Fund a deal")
def fund_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Retrieve pending deal owned by current user
    deal = (
        db.query(Deal)
          .filter(Deal.id == deal_id, Deal.creator_id == current_user.id)
          .first()
    )
    if not deal or deal.status != DealStatus.pending:
        raise HTTPException(status_code=400, detail="Deal not found or cannot be funded.")

    # Check wallet balance
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if wallet.balance < deal.amount:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

    # Deduct amount and update deal status
    wallet.balance -= deal.amount
    deal.status = DealStatus.active

    # Record transaction
    transaction = WalletTransaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        amount=deal.amount,
        transaction_type="escrow_fund",
        description=f"Funded Deal {deal.id}",
    )
    db.add(transaction)
    db.commit()

    # TODO: re-enable notifications once wired up
    # send_email(to=counterparty.email, subject="Deal Funded", body="…")
    # create_notification(db=db, user_id=counterparty.id, title="Deal Funded", message="…")

    return {"message": "Deal funded successfully."}


@router.post("/{deal_id}/deliver", summary="Mark a deal as delivered")
def mark_delivered(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deal = (
        db.query(Deal)
          .filter(Deal.id == deal_id, Deal.counterparty_id == current_user.id)
          .first()
    )
    if not deal or deal.status != DealStatus.active:
        raise HTTPException(status_code=400, detail="Deal not found or cannot be marked delivered.")

    deal.status = DealStatus.completed
    db.commit()

    # TODO: re-enable notifications once wired up
    # send_email(to=creator.email, subject="Deal Delivered", body="…")
    # create_notification(db=db, user_id=creator.id, title="Deal Delivered", message="…")

    return {"message": "Deal marked as delivered."}


@router.post("/{deal_id}/release", summary="Release funds for a completed deal")
def release_funds(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deal = (
        db.query(Deal)
          .filter(Deal.id == deal_id, Deal.creator_id == current_user.id)
          .first()
    )
    if not deal or deal.status != DealStatus.completed:
        raise HTTPException(status_code=400, detail="Deal not ready for release.")

    # Credit seller wallet
    seller_wallet = db.query(Wallet).filter(Wallet.user_id == deal.counterparty_id).first()
    seller_wallet.balance += deal.amount

    transaction = WalletTransaction(
        wallet_id=seller_wallet.id,
        user_id=deal.counterparty_id,
        amount=deal.amount,
        transaction_type="escrow_release",
        description=f"Released funds for Deal {deal.id}",
    )
    db.add(transaction)
    db.commit()

    # TODO: re-enable notifications once wired up
    # send_email(to=counterparty.email, subject="Funds Released", body="…")
    # create_notification(db=db, user_id=counterparty.id, title="Funds Released", message="…")

    return {"message": "Funds released to seller."}


@router.post("/{deal_id}/dispute", summary="Raise a dispute on a deal")
def raise_dispute(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deal = (
        db.query(Deal)
          .filter(
              Deal.id == deal_id,
              ((Deal.creator_id == current_user.id) | (Deal.counterparty_id == current_user.id))
          )
          .first()
    )
    if not deal or deal.status not in (DealStatus.active, DealStatus.completed):
        raise HTTPException(status_code=400, detail="Cannot dispute this deal.")

    deal.status = DealStatus.disputed
    db.commit()

    # TODO: re-enable notifications once wired up
    # for user in (creator, counterparty):
    #     send_email(…)
    #     create_notification(…)

    return {"message": "Deal marked as disputed."}