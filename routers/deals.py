File: routers/deals_notifications.py (upgrade for notifications)

from fastapi import APIRouter, Depends, HTTPException from sqlalchemy.orm import Session from core.database import get_db from core.security import get_current_user from models.deal import Deal, DealStatus from models.wallet import Wallet from models.wallet_transaction import WalletTransaction from schemas.deal import DealCreate, DealOut from models.user import User from utils.notifications import send_email, create_notification

router = APIRouter(prefix="/deals", tags=["Deals"])

(existing create_deal remains unchanged)

─────────── FUND DEAL WITH NOTIFICATION ───────────

@router.post("/{deal_id}/fund") def fund_deal(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): deal = db.query(Deal).filter(Deal.id == deal_id, Deal.creator_id == current_user.id).first() if not deal or deal.status != DealStatus.pending: raise HTTPException(status_code=400, detail="Deal not found or cannot be funded.")

wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
if wallet.balance < deal.amount:
    raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

wallet.balance -= deal.amount
deal.status = DealStatus.active

transaction = WalletTransaction(
    wallet_id=wallet.id,
    user_id=current_user.id,
    amount=deal.amount,
    transaction_type="escrow_fund",
    description=f"Funded Deal {deal.id}"
)
db.add(transaction)
db.commit()

# Notify counterparty
counterparty = db.query(User).filter(User.id == deal.counterparty_id).first()
send_email(
    to=counterparty.email,
    subject="Dealcross: Deal Funded",
    body=f"Hello {counterparty.full_name or 'User'},\n\nThe deal '{deal.title}' has been funded. Please proceed with your delivery."
)
create_notification(
    db=db,
    user_id=counterparty.id,
    title="Deal Funded",
    message=f"The deal '{deal.title}' has been funded."
)

return {"message": "Deal funded successfully."}

─────────── DELIVER DEAL WITH NOTIFICATION ───────────

@router.post("/{deal_id}/deliver") def mark_delivered(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): deal = db.query(Deal).filter(Deal.id == deal_id, Deal.counterparty_id == current_user.id).first() if not deal or deal.status != DealStatus.active: raise HTTPException(status_code=400, detail="Deal not found or cannot be marked delivered.")

deal.status = DealStatus.completed
db.commit()

# Notify creator
creator = db.query(User).filter(User.id == deal.creator_id).first()
send_email(
    to=creator.email,
    subject="Dealcross: Deal Delivered",
    body=f"Hello {creator.full_name or 'User'},\n\nThe deal '{deal.title}' has been marked as delivered. Please review and release funds."
)
create_notification(
    db=db,
    user_id=creator.id,
    title="Deal Delivered",
    message=f"The deal '{deal.title}' has been marked as delivered."
)

return {"message": "Deal marked as delivered."}

─────────── RELEASE FUNDS WITH NOTIFICATION ───────────

@router.post("/{deal_id}/release") def release_funds(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): deal = db.query(Deal).filter(Deal.id == deal_id, Deal.creator_id == current_user.id).first() if not deal or deal.status != DealStatus.completed: raise HTTPException(status_code=400, detail="Deal not ready for release.")

seller_wallet = db.query(Wallet).filter(Wallet.user_id == deal.counterparty_id).first()
seller_wallet.balance += deal.amount

transaction = WalletTransaction(
    wallet_id=seller_wallet.id,
    user_id=deal.counterparty_id,
    amount=deal.amount,
    transaction_type="escrow_release",
    description=f"Released funds for Deal {deal.id}"
)
db.add(transaction)
db.commit()

# Notify counterparty (seller)
counterparty = db.query(User).filter(User.id == deal.counterparty_id).first()
send_email(
    to=counterparty.email,
    subject="Dealcross: Funds Released",
    body=f"Hello {counterparty.full_name or 'User'},\n\nThe funds for deal '{deal.title}' have been released to your wallet."
)
create_notification(
    db=db,
    user_id=counterparty.id,
    title="Funds Released",
    message=f"The funds for deal '{deal.title}' have been released to your wallet."
)

return {"message": "Funds released to seller."}

─────────── RAISE DISPUTE WITH NOTIFICATION ───────────

@router.post("/{deal_id}/dispute") def raise_dispute(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)): deal = db.query(Deal).filter( Deal.id == deal_id, ((Deal.creator_id == current_user.id) | (Deal.counterparty_id == current_user.id)) ).first() if not deal or deal.status not in [DealStatus.active, DealStatus.completed]: raise HTTPException(status_code=400, detail="Cannot dispute this deal.")

deal.status = DealStatus.disputed
db.commit()

# Notify both parties
creator = db.query(User).filter(User.id == deal.creator_id).first()
counterparty = db.query(User).filter(User.id == deal.counterparty_id).first()

for user in [creator, counterparty]:
    send_email(
        to=user.email,
        subject="Dealcross: Deal Disputed",
        body=f"Hello {user.full_name or 'User'},\n\nThe deal '{deal.title}' has been marked as disputed."
    )
    create_notification(
        db=db,
        user_id=user.id,
        title="Deal Disputed",
        message=f"The deal '{deal.title}' has been marked as disputed."
    )

return {"message": "Deal marked as disputed."}

