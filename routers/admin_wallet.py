# File: routers/admin_wallet.py

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models.admin_wallet import AdminWallet
from models.admin_wallet_log import AdminWalletLog
from models.user import User
from core.security import get_current_user

router = APIRouter(prefix="/admin-wallet", tags=["Admin Wallet"])

# ─────────── INPUT SCHEMA ───────────
class WalletAdjustment(BaseModel):
    amount: float
    action: str  # "credit" or "debit"
    description: str

# ─────────── ADMIN-ONLY ACCESS ───────────
def require_admin(user: User):
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only.")
    return user

# ─────────── MANUAL CREDIT / DEBIT ───────────
@router.post("/adjust", summary="Manually credit or debit the admin wallet")
async def adjust_admin_wallet(
    adjustment: WalletAdjustment,
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    amount = Decimal(adjustment.amount)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive.")

    wallet = await AdminWallet.first()
    if not wallet:
        wallet = await AdminWallet.create(balance=0)

    if adjustment.action == "credit":
        wallet.balance += amount
    elif adjustment.action == "debit":
        if wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient admin wallet balance.")
        wallet.balance -= amount
    else:
        raise HTTPException(status_code=400, detail="Action must be 'credit' or 'debit'.")

    wallet.last_updated_by = current_user
    await wallet.save()

    # Log the adjustment
    await AdminWalletLog.create(
        amount=amount,
        action=adjustment.action,
        description=adjustment.description,
        admin_wallet=wallet,
        triggered_by=current_user
    )

    return {
        "message": f"Wallet {adjustment.action}ed successfully.",
        "new_balance": float(wallet.balance)
    }

# ─────────── VIEW LOGS (OPTIONAL) ───────────
@router.get("/logs", summary="View admin wallet logs")
async def view_logs(current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    logs = await AdminWalletLog.all().prefetch_related("triggered_by").order_by("-created_at")
    return [
        {
            "amount": float(log.amount),
            "action": log.action,
            "description": log.description,
            "by": log.triggered_by.email if log.triggered_by else "system",
            "timestamp": log.created_at,
        }
        for log in logs
    ]