# File: schemas/user.py

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Shared user fields
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# For creating a user
class UserCreate(UserBase):
    password: str

# For reading user data (e.g. admin views)
class UserOut(UserBase):
    id: int
    is_active: bool
    is_banned: bool = False
    role: Optional[str] = "user"
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# For admin updates
class UserAdminUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_banned: Optional[bool] = None
    approval_note: Optional[str] = None
    ban_reason: Optional[str] = None
