from utils.fee_calculator import apply_escrow_fee
from models.fee_transaction import FeeType  # Optional, if needed for clarity

@router.post("/create", summary="Create a new deal between users")
def create_deal(
    payload: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a deal with another user. Escrow fee is deducted upfront and sent to admin wallet.
    """
    counterparty = db.query(User).filter(User.id == payload.counterparty_id).first()
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found")

    existing_deal = db.query(Deal).filter(
        Deal.creator_id == current_user.id,
        Deal.counterparty_id == payload.counterparty_id,
        Deal.title == payload.title,
        Deal.status.in_([DealStatus.pending, DealStatus.active])
    ).first()

    if existing_deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A similar deal is already in progress with this counterparty."
        )

    # ✅ Deduct escrow fee
    net_amount, fee = apply_escrow_fee(db, current_user, payload.amount)
    fee_rate = "3%" if current_user.role.value == "basic" else "2%"

    # ✅ Create deal with net amount
    new_deal = Deal(
        title=payload.title,
        amount=net_amount,
        description=payload.description,
        public_deal=payload.public_deal,
        creator_id=current_user.id,
        counterparty_id=payload.counterparty_id
    )

    # ✅ Auto-fraud detection
    if basic_fraud_check(new_deal):
        new_deal.is_flagged = True
        db.add(AuditLog(
            admin_id=None,
            action="DEAL AUTO-FLAGGED (FRAUD RULE)",
            target_type="DEAL",
            target_id=new_deal.id
        ))

    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)

    # ✅ Enhanced response
    return {
        "message": "Deal created successfully",
        "data": {
            "deal_id": new_deal.id,
            "title": new_deal.title,
            "original_amount": payload.amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "user_tier": current_user.role.value,
            "net_amount": net_amount
        }
    }
