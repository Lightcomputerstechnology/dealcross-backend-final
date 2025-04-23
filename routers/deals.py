@router.get("/tracker", summary="Get all your active and past deals")
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all deals involving the current user.
    Adds status badges and readable timestamps.
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

    return {
        "message": "Deals retrieved successfully",
        "data": [
            {
                "deal_id": deal.id,
                "title": deal.title,
                "amount": float(deal.amount),
                "status": get_status_badge(deal.status),
                "is_flagged": deal.is_flagged,
                "created_at": deal.created_at.strftime("%B %d, %Y, %I:%M %p"),
                "counterparty_id": deal.counterparty_id
            }
            for deal in deals
        ]
                         }
