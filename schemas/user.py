from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from models.user import UserRole

# Shared User Base
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.user
    status: str = "active"
    cumulative_sales: float = 0.00

    model_config = {
        "from_attributes": True
    }

# User Creation
class UserCreate(UserBase):
    password: str

# User Update (self-service)
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# Admin User Update
class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[str] = None
    full_name: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# Output Schema
class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
