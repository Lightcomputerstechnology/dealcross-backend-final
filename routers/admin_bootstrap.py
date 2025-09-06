# routers/admin_bootstrap.py
from fastapi import APIRouter, Header, HTTPException
from tortoise.transactions import in_transaction
from models.admin import Admin
from passlib.hash import bcrypt
import os

router = APIRouter(prefix="/admin", tags=["Admin Bootstrap"])

BOOT_TOKEN = os.getenv("ADMIN_BOOTSTRAP_TOKEN")  # set this in Render env

@router.post("/bootstrap")
async def bootstrap_admin(x_bootstrap_token: str = Header(None)):
    # Simple guard
    if not BOOT_TOKEN or x_bootstrap_token != BOOT_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

    admin_email = "admin@dealcross.com"
    admin_password = "AdminPass123!"

    async with in_transaction():
        existing = await Admin.get_or_none(email=admin_email)
        if existing:
            return {"ok": True, "detail": "Admin already exists"}

        await Admin.create(
            email=admin_email,
            hashed_password=bcrypt.hash(admin_password),
            is_superuser=True,
            is_active=True,
        )
        return {"ok": True, "detail": f"Admin created: {admin_email} / {admin_password}"}