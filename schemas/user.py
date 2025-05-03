from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

    model_config = {"from_attributes": True}


class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[str] = None

    model_config = {"from_attributes": True}