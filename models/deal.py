Step 1: Update your Deal model (models/deal.py)

from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey from database import Base

class Deal(Base): tablename = 'deals'

id = Column(Integer, primary_key=True, index=True)
title = Column(String, index=True)
amount = Column(Float)
status = Column(String)
counterparty_email = Column(String)
description = Column(String)
public_deal = Column(Boolean, default=False)  # NEW FIELD

Step 2: Update your Deal schema (schemas/deal.py)

from pydantic import BaseModel

class DealBase(BaseModel): title: str amount: float status: str counterparty_email: str description: str public_deal: bool = False

class DealOut(DealBase): id: int

class Config:
    orm_mode = True

Step 3: Create a public deals route (routers/deal.py)

from fastapi import APIRouter, Depends from sqlalchemy.orm import Session from database import get_db from models.deal import Deal from schemas.deal import DealOut from typing import List

router = APIRouter()

@router.get("/deals/public", response_model=List[DealOut]) def get_public_deals(db: Session = Depends(get_db)): return db.query(Deal).filter(Deal.public_deal == True).all()

Step 4: Make sure to include router in main.py

from routers import deal  # if deal.py is in routers folder app.include_router(deal.router)

Step 5: Run migration (if using Alembic)

alembic revision --autogenerate -m "add public_deal field"

alembic upgrade head

