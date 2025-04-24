from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.user
    status: str = "active"
    cumulative_sales: float = 0.00

    model_config = {"from_attributes": True}

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

    model_config = {"from_attributes": True}

class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[str] = None
    full_name: Optional[str] = None

    model_config = {"from_attributes": True}

class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"