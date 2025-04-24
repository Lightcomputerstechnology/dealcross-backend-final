from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.deal import Deal
from models.user import User
router = APIRouter(prefix="/deals", tags=["Deals"])
@router.get("/tracker", summary="Get all your active and past deals")
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all deals involving the current user.
    Adds status badges, readable timestamps, counterparty details, fees, role, and deal type.
    """
    deals = db.query(Deal).filter(
        (Deal.creator_id == current_user.id) | 
        (Deal.counterparty_id == current_user.id)
    ).order_by(Deal.created_at.desc()).all()

    def get_status_badge(status):
        return {
            "pending": {"label": "Pending", "color": "yellow"},
            "active": {"label": "Active", "color": "blue"},
            "completed": {"label": "Completed", "color": "green"},
            "disputed": {"label": "Disputed", "color": "red"}
        }.get(status.value, {"label": status.value, "color": "gray"})

    deal_list = []
    for deal in deals:
        counterparty = db.query(User).filter(User.id == deal.counterparty_id).first()
        fee_deducted = float(getattr(deal, 'fee_amount', 0.0))
        progress_percent = getattr(deal, 'progress_percent', None)
        deal_type = getattr(deal, 'deal_type', 'escrow')

        role = "seller" if deal.creator_id == current_user.id else "buyer"

        deal_data = {
            "deal_id": deal.id,
            "title": deal.title,
            "amount": float(deal.amount),
            "status": get_status_badge(deal.status),
            "is_flagged": deal.is_flagged,
            "created_at": deal.created_at.strftime("%B %d, %Y, %I:%M %p"),
            "counterparty": {
                "id": f"USR-{str(counterparty.id).zfill(5)}-DC" if counterparty else None,
                "username": counterparty.username if counterparty else None
            },
            "fee_deducted": fee_deducted,
            "progress_percent": progress_percent,
            "deal_type": deal_type,
            "role": role,
            "security": {
                "flagged": deal.is_flagged,
                "badge": "High Risk" if deal.is_flagged else "Verified"
            }
        }
        deal_list.append(deal_data)

    return {
        "message": "Deals retrieved successfully",
        "data": deal_list
        }
