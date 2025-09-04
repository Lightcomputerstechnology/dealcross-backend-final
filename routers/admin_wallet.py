# File: routers/admin_wallet.py

from typing import Dict, Any, Optional, List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.security import get_current_user  # Supabase-aware claims
from core.supabase_client import get_profile_is_admin  # server-side admin check
from models.admin_wallet import AdminWallet
from models.admin_wallet_log import AdminWalletLog
from models.user import User

router = APIRouter(prefix="/admin-wallet", tags=["Admin Wallet"])

# ─────────── INPUT SCHEMA ───────────
class WalletAdjustment(BaseModel):
    amount: float
    action: str  # "credit" or "debit"
    description: str

# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user

# ─────────── ADMIN-ONLY ACCESS (Supabase profiles.is_admin or local flag) ───────────
async def require_admin(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    supa_user_id = claims.get("sub")
    is_admin = False
    if supa_user_id:
        flag = get_profile_is_admin(supa_user_id)
        is_admin = bool(flag)

    if not is_admin and (getattr(db_user, "is_admin", False) or getattr(db_user, "role", "") == "admin"):
        is_admin = True

    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")
    return db_user

# ─────────── MANUAL CREDIT / DEBIT ───────────
@router.post("/adjust", summary="Manually credit or debit the admin wallet")
async def adjust_admin_wallet(
    adjustment: WalletAdjustment,
    admin_user: User = Depends(require_admin),
):
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

    # If your model has a FK for last_updated_by, keep it; otherwise remove this line
    wallet.last_updated_by = admin_user  # type: ignore[attr-defined]
    await wallet.save()

    # Log the adjustment
    await AdminWalletLog.create(
        amount=amount,
        action=adjustment.action,
        description=adjustment.description,
        admin_wallet=wallet,
        triggered_by=admin_user
    )

    return {
        "message": f"Wallet {adjustment.action}ed successfully.",
        "new_balance": float(wallet.balance)
    }

# ─────────── VIEW LOGS (OPTIONAL) ───────────
@router.get("/logs", summary="View admin wallet logs")
async def view_logs(_: User = Depends(require_admin)):
    logs = await AdminWalletLog.all().prefetch_related("triggered_by").order_by("-created_at")
    return [
        {
            "amount": float(log.amount),
            "action": log.action,
            "description": log.description,
            "by": (log.triggered_by.email if getattr(log, "triggered_by", None) else "system"),
            "timestamp": log.created_at,
        }
        for log in logs
    ]
