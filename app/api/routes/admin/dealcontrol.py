from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.deal import Deal
from typing import List

router = APIRouter()

@router.get("/pending-deals")
def get_pending_deals(db: Session = Depends(get_db)):
    pending = db.query(Deal).filter(Deal.status == "Pending").all()
    return [
        {
            "id": d.id,
            "title": d.title,
            "amount": d.amount,
            "status": d.status,
            "public_deal": d.public_deal,
            "counterparty_email": d.counterparty_email,
        }
        for d in pending
    ]

@router.post("/approve-deal/{deal_id}")
def approve_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "Approved"
    db.commit()
    return {"message": f"Deal {deal_id} approved."}

@router.post("/reject-deal/{deal_id}")
def reject_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = "Rejected"
    db.commit()
    return {"message": f"Deal {deal_id} rejected."}
