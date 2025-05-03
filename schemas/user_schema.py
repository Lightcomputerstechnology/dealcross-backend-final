# File: schemas/user_schema.py

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


# === Role Enumeration for Validation (Optional) ===
class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    auditor = "auditor"
    admin = "admin"


# === Base Shared User Schema ===
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.user
    status: Optional[str] = "active"
    cumulative_sales: Optional[float] = 0.00


# === Create User Payload ===
class UserCreate(UserBase):
    password: str
    referrer_code: Optional[str] = None  # ✅ Added for referral support


# === User Output Schema (Admin / Frontend) ===
class UserOut(UserBase):
    id: int
    is_active: bool = True
    is_banned: bool = False
    is_admin: bool = False
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None
    referral_code: Optional[str] = None  # ✅ Unique user code
    referred_by: Optional[int] = None    # ✅ Referrer's user ID
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
    role: Optional[UserRole] = None
    status: Optional[str] = None
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


# === User Self Update Payload ===
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

    model_config = {
        "from_attributes": True
    }