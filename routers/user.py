from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter(prefix="/user", tags=["User Settings"])

# === Get User Settings ===
@router.get("/settings", summary="View user tier and fee rates")
def get_user_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns the user's current tier and applicable fee rates:

    - Funding fee
    - Escrow fee
    - Share buyer fee
    - Share seller fee (post $1,000 cumulative)
    """
    tier = current_user.role.value  # 'basic', 'pro', etc.

    # Define fee rates based on tier
    fee_rates = {
        "funding": "2%" if tier == "basic" else "1.5%",
        "escrow": "3%" if tier == "basic" else "2%",
        "share_buyer": "2%" if tier == "basic" else "1.5%",
        "share_seller": "1% (after $1,000)" if tier == "basic" else "0.75% (after $1,000)"
    }

    return {
        "message": "User settings retrieved successfully",
        "data": {
            "user_id": current_user.id,
            "tier": tier,
            "fee_rates": fee_rates
        }
    }
