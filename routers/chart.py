from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user  # Supabase-aware claims
from models.user import User
from models.chart import ChartPoint
from schemas.chart import ChartPointOut

router = APIRouter(prefix="/chart", tags=["Chart"])


# Map verified JWT claims -> local DB User
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


# Fetch all chart points for dashboard (auth required)
@router.get("/", response_model=List[ChartPointOut])
async def get_chart_data(_: User = Depends(resolve_db_user)):
    points = await ChartPoint.all().order_by("-created_at")
    return [await ChartPointOut.from_tortoise_orm(p) for p in points]
