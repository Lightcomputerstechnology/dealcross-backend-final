# File: schemas/user_schema.py

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# === Base Shared User Schema ===
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# === Create User Payload ===
class UserCreate(UserBase):
    password: str
    referrer_code: Optional[str] = None  # ✅ Added for referral support


# === User Output Schema (Admin / Frontend) ===
class UserOut(UserBase):
    id: int
    is_active: bool
    is_banned: bool = False
    is_admin: bool = False
    status: Optional[str] = "active"  # e.g., active, banned
    role: Optional[str] = "user"
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None
    referral_code: Optional[str] = None  # ✅ Unique code generated
    referred_by: Optional[int] = None    # ✅ Referrer user ID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# === Admin-only Update Payload ===
class UserAdminUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_banned: Optional[bool] = None
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


# === User Self Update Payload ===
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
