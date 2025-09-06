# File: routers/admin_bootstrap.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models.admin import Admin
from passlib.hash import bcrypt
import os

router = APIRouter(prefix="/_bootstrap", tags=["_bootstrap"])

class AdminSeed(BaseModel):
    email: str
    password: str
    token: str

@router.post("/seed-admin")
async def seed_admin(payload: AdminSeed):
    if payload.token != os.getenv("BOOTSTRAP_TOKEN", ""):
        raise HTTPException(status_code=403, detail="Forbidden")
    exists = await Admin.get_or_none(email=payload.email)
    if exists:
        return {"message": "Admin already exists"}
    await Admin.create(
        email=payload.email,
        hashed_password=bcrypt.hash(payload.password),
        is_superuser=True,
        is_active=True,
    )
    return {"message": "Admin created"}
