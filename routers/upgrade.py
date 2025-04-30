# File: routers/upgrade.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.auth import get_current_user
from core.database import get_db
from models.user import User

router = APIRouter()

class UpgradeRequest(BaseModel):
    plan: str  # 'pro' or 'business'
    method: str  # 'card', 'paystack', etc.

@router.post("/users/upgrade-plan")
def upgrade_plan(data: UpgradeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.plan not in ["pro", "business"]:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    # Optional: Validate payment method if needed

    current_user.subscription = data.plan
    db.commit()
    return {"message": f"Account upgraded to {data.plan.capitalize()} successfully."}
