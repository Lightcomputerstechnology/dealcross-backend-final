# File: schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    password: str  # For registration

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

    model_config = {
        "from_attributes": True
    }

class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
