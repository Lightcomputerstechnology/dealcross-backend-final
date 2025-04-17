from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}
