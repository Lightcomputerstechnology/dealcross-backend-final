# File: schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole


class LegacyUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.user
    status: str = "active"
    created_at: datetime

    model_config = {"from_attributes": True}


class LegacyUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    status: Optional[str] = None

    model_config = {"from_attributes": True}
