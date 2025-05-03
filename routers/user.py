# File: routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, get_password_hash
from schemas.user import UserOut, UserUpdate, UserAdminUpdate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User  # For type hinting only

from models import user as user_model  # Import module instead of direct model to avoid circular import

router = APIRouter(prefix="/user", tags=["User Management"])


# === View Current User Profile ===
@router.get("/profile", response_model=UserOut, summary="Get current user profile")
def get_profile(current_user: "User" = Depends(get_current_user)):
    return current_user


# === Update Current User Profile ===
@router.put("/profile/update", response_model=UserOut, summary="Update current user profile")
def update_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user)
):
    if updates.username:
        current_user.username = updates.username
    if updates.email:
        current_user.email = updates.email
    if updates.password:
        current_user.hashed_password = get_password_hash(updates.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user


# === Get User Settings (Fees & Tier) ===
@router.get("/settings", summary="View user tier and fee rates")
def get_user_settings(
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user)
):
    tier = current_user.role.value if hasattr(current_user.role, "value") else current_user.role
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


# === Admin: List All Users ===
@router.get("/admin/users", summary="Admin: List all users")
def list_users(
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return db.query(user_model.User).all()


# === Admin: Update User Role / Status ===
@router.put("/admin/update/{user_id}", summary="Admin: Update user role or status")
def admin_update_user(
    user_id: int,
    updates: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if updates.username:
        user.username = updates.username
    if updates.email:
        user.email = updates.email
    if updates.is_active is not None:
        user.is_active = updates.is_active
    if updates.is_admin is not None:
        user.is_admin = updates.is_admin

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}
