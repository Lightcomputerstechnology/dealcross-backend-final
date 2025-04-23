# File: schemas/user_admin.py

from pydantic import BaseModel
from datetime import datetime

class UserAdminBase(BaseModel):
    username: str
    email: str
    role: str

    model_config = {
        "from_attributes": True  # For SQLAlchemy integration (Pydantic v2)
    }

class UserAdminCreate(UserAdminBase):
    password: str  # Add password for creating new admin users

class UserAdminUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None
    password: str | None = None

    model_config = {
        "from_attributes": True
    }

class UserAdminOut(UserAdminBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
