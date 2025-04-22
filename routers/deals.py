# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from models.deal import Deal, DealStatus
from models.user import User
from schemas.deal import DealCreate, DealOut

router = APIRouter()

@router.post("/create", response_model=DealOut)
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if counterparty exists
    counterparty = db.query(User).filter(User.id == payload.counterparty_id).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

    # Check for duplicate deal
    existing_deal = db.query(Deal).filter(
        Deal.creator_id == current_user.id,
        Deal.counterparty_id == payload.counterparty_id,
        Deal.title == payload.title,
        Deal.status.in_([DealStatus.pending, DealStatus.active])
    ).first()

    if existing_deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A similar deal is already in progress with this counterparty."
        )

    # Create new deal
    new_deal = Deal(
        title=payload.title,
        amount=payload.amount,
        description=payload.description,
        public_deal=payload.public_deal,
        creator_id=current_user.id,
        counterparty_id=payload.counterparty_id
    )

    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)

    return new_deal

@router.get("/tracker", response_model=List[DealOut])
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deals = db.query(Deal).filter(
        (Deal.creator_id == current_user.id) |
        (Deal.counterparty_id == current_user.id)
    ).all()
    return deals

@router.get("/public", response_model=List[DealOut])
def get_public_deals(db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.public_deal == True).all()
