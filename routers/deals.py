# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.deal import Deal
from models.user import User
from schemas.deal_schema import DealCreate, DealOut

router = APIRouter()


@router.post("/create", response_model=DealOut)
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    counterparty = db.query(User).filter(User.email == payload.counterparty_email).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

    new_deal = Deal(
        title=payload.title,
        amount=payload.amount,
        status=payload.status,
        description=payload.description,
        counterparty_email=payload.counterparty_email,
        public_deal=payload.public_deal
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
    user_email = current_user.email
    deals = db.query(Deal).filter(Deal.counterparty_email == user_email).all()
    return deals


@router.get("/public", response_model=List[DealOut])
def get_public_deals(db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.public_deal == True).all()
