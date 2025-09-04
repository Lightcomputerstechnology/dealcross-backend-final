# File: app/routers/auth.py
from fastapi import APIRouter, Depends
from app.core.security import get_current_user, require_admin, AuthUser

router = APIRouter()

@router.get("/me")
async def read_me(user: AuthUser = Depends(get_current_user)):
    """
    Returns a shape compatible with your frontend expectations.
    You can enrich this with DB info (wallet, role, etc.) if needed.
    """
    # If you still need a 'role' for legacy UI paths, you can set it using a claim.
    claims = user.get("claims", {})
    role = "admin" if (claims.get("is_admin") or claims.get("user_metadata", {}).get("is_admin")) else "user"
    return {
        "id": user.get("id"),
        "email": user.get("email"),
        "role": role,
    }

@router.get("/me/admin-check")
async def admin_check(_: AuthUser = Depends(require_admin)):
    return {"ok": True, "role": "admin"}
