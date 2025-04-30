# File: routers/chart.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from tortoise.expressions import Q

from models.chart import ChartPoint
from schemas.chart import ChartPointCreate, ChartPointOut
from core.security import get_current_user
from models.user import User

router = APIRouter(prefix="/admin/charts", tags=["Admin Charts"])

@router.get("/", response_model=List[ChartPointOut])
async def get_all_chart_data(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return await ChartPoint.all()

@router.get("/label/{label}", response_model=List[ChartPointOut])
async def get_chart_data_by_label(label: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return await ChartPoint.filter(label=label).order_by("-timestamp")

@router.post("/", response_model=ChartPointOut)
async def create_chart_point(data: ChartPointCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    new_point = await ChartPoint.create(**data.dict())
    return new_point