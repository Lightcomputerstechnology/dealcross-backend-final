# File: schemas/user_schema.py

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import UserRole

# === Base Schema Shared by All ===
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.user
    status: str = "active"
    cumulative_sales: float = 0.00

    model_config = {"from_attributes": True}


# === Used during Signup ===
class UserCreate(UserBase):
    password: str
    referrer_code: Optional[str] = None  # ✅ Supports referral signup


# === Output Schema Used in /me, Admin View, etc. ===
class UserOut(UserBase):
    id: int
    created_at: datetime
    referral_code: Optional[str] = None
    referred_by: Optional[int] = None
    is_active: bool = True
    is_banned: bool = False
    is_admin: bool = False
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None

    model_config = {"from_attributes": True}


# === User Self-Update Schema ===
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

    model_config = {"from_attributes": True}


# === Admin-Only Update Schema ===
class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[str] = None
    full_name: Optional[str] = None

    model_config = {"from_attributes": True}


# === Token Output Schema ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
