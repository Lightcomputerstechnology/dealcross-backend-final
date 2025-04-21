# File: app/api/routes/admin/dealcontrol.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.deal import Deal
from schemas.deal import DealOut, DealAdminUpdate

router = APIRouter()


@router.get("/pending-deals", response_model=List[DealOut])
def get_pending_deals(db: Session = Depends(get_db)):
    deals = db.query(Deal).filter(Deal.status == "Pending").order_by(Deal.created_at.desc()).all()
    return deals


@router.put("/approve-deal/{deal_id}", response_model=DealOut)
def approve_deal(deal_id: int, update: DealAdminUpdate = None, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.status = "Approved"
    if update and update.approval_note:
        deal.approval_note = update.approval_note

    db.commit()
    db.refresh(deal)
    return deal


@router.put("/reject-deal/{deal_id}", response_model=DealOut)
def reject_deal(deal_id: int, update: DealAdminUpdate = None, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.status = "Rejected"
    if update and update.approval_note:
        deal.approval_note = update.approval_note

    db.commit()
    db.refresh(deal)
    return deal
