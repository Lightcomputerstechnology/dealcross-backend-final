from fastapi import APIRouter, HTTPException, Depends, status
from tortoise.exceptions import DoesNotExist
from typing import List, Dict, Any, Optional

from core.security import get_current_user  # ✅ now returns Supabase/legacy JWT claims dict
from core.security import get_password_hash
from core.supabase_client import get_profile_is_admin  # ✅ server-side DB check for is_admin

from schemas.user import UserOut, UserUpdate, UserAdminUpdate
from models.user import User, UserRole

router = APIRouter(prefix="/user", tags=["User Management"])


# --------------------------- Helpers ---------------------------

async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    """
    Map an authenticated JWT (Supabase or legacy) to your local User row.
    Strategy:
      1) Prefer email from JWT claims
      2) Fetch User by email. If not found, fail clearly (no auto-create).
         -> This protects your schema from silent bad data. You can implement
            an explicit onboarding endpoint if you want to auto-provision.
    """
    email: Optional[str] = claims.get("email")
    if not email:
        # Some legacy tokens might not carry email; adjust if you map by username instead.
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")

    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User record not found for this account. Please complete onboarding or contact support."
        )
    return user


async def require_admin_from_supabase_or_local(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    """
    Server-side admin verification:
      - First, checks Supabase public.profiles.is_admin using SERVICE ROLE.
      - Fallback: uses your local user.is_admin if present.
    Returns the db_user on success.
    """
    supa_user_id = claims.get("sub")  # Supabase uses 'sub' as auth.users.id
    is_admin = False

    if supa_user_id:
        flag = get_profile_is_admin(supa_user_id)  # None or bool
        is_admin = bool(flag)

    # Fallback to local flag if you already store it on your User model
    if not is_admin and getattr(db_user, "is_admin", False):
        is_admin = True

    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return db_user


# --------------------------- Endpoints ---------------------------

# === Current User Profile ===
@router.get("/profile", response_model=UserOut)
async def get_profile(current_user: User = Depends(resolve_db_user)):
    return await UserOut.from_tortoise_orm(current_user)


@router.put("/profile/update", response_model=UserOut)
async def update_profile(
    updates: UserUpdate,
    current_user: User = Depends(resolve_db_user),
):
    for field, value in updates.model_dump(exclude_unset=True).items():
        if field == "password":
            setattr(current_user, "hashed_password", get_password_hash(value))
        else:
            setattr(current_user, field, value)

    await current_user.save()
    return await UserOut.from_tortoise_orm(current_user)


# === User Fee Settings ===
@router.get("/settings")
async def get_user_settings(current_user: User = Depends(resolve_db_user)):
    tier = current_user.role.value if isinstance(current_user.role, UserRole) else current_user.role
    fee_rates = {
        "funding":      "2%" if tier == "basic" else "1.5%",
        "escrow":       "3%" if tier == "basic" else "2%",
        "share_buyer":  "2%" if tier == "basic" else "1.5%",
        "share_seller": "1% (after $1,000)" if tier == "basic" else "0.75% (after $1,000)",
    }

    return {
        "message": "User settings retrieved successfully",
        "data": {
            "user_id": current_user.id,
            "tier": tier,
            "fee_rates": fee_rates,
        }
    }


# === Admin: List All Users ===
@router.get("/admin/users", response_model=List[UserOut])
async def list_users(_: User = Depends(require_admin_from_supabase_or_local)):
    users = await User.all()
    return [await UserOut.from_tortoise_orm(u) for u in users]


# === Admin: Update Any User ===
@router.put("/admin/update/{user_id}", response_model=UserOut)
async def admin_update_user(
    user_id: int,
    updates: UserAdminUpdate,
    _: User = Depends(require_admin_from_supabase_or_local),
):
    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await user.save()
    return await UserOut.from_tortoise_orm(user)
