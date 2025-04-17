# File: routers/deals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.deal import Deal
from models.user import User
from schemas.deal_schema import DealCreate
from core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_deal(payload: DealCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    counterparty = db.query(User).filter(User.email == payload.counterparty_email).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

    deal = Deal(
        title=payload.title,
        amount=payload.amount,
        escrow_type=payload.escrow_type,
        role=payload.role,
        creator_id=current_user.id,
        counterparty_id=counterparty.id,
        status="Pending"
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return {"message": "Deal created", "deal_id": deal.id}

@router.get("/tracker")
def get_my_deals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deals = db.query(Deal).filter((Deal.creator_id == current_user.id) | (Deal.counterparty_id == current_user.id)).all()
    return [
        {
            "title": d.title,
            "amount": d.amount,
            "status": d.status,
            "created_at": d.created_at.strftime("%Y-%m-%d")
        }
        for d in deals
    ]
