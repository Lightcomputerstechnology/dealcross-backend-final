# routers/admin_bootstrap.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, constr
from os import getenv
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError, OperationalError
from tortoise import Tortoise

# Import your Admin model (table = "admins")
from models.admin import Admin

router = APIRouter(prefix="/_bootstrap", tags=["bootstrap"])

class SeedAdminIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    token: str

@router.get("/ping")
async def ping():
    """Quick health for the bootstrap router."""
    try:
        # verify Tortoise is up and the DB responds
        await Tortoise.get_connection("default").execute_query("SELECT 1;")
        return {"ok": True, "db": "up"}
    except Exception as e:
        return {"ok": False, "db": "down", "error": str(e)}

@router.post("/seed-admin")
async def seed_admin(payload: SeedAdminIn):
    # 1) Token check (403 on bad token)
    expected = getenv("BOOTSTRAP_TOKEN")
    if not expected:
        # Misconfiguration – tell you clearly
        raise HTTPException(status_code=500, detail="BOOTSTRAP_TOKEN not set on server")
    if payload.token.strip() != expected.strip():
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2) Try to create (idempotent)
    try:
        existing = await Admin.get_or_none(email=payload.email)
        if existing:
            return {"ok": True, "message": "already_exists"}

        admin = await Admin.create(
            email=payload.email,
            hashed_password=bcrypt.hash(payload.password),
            is_superuser=True,
            is_active=True,
        )
        return {"ok": True, "message": "created", "id": admin.id}

    except IntegrityError as e:
        # Unique constraint, etc.
        return {"ok": True, "message": "already_exists", "info": "integrity_error"}
    except OperationalError as e:
        # Table missing or DB not reachable
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    except Exception as e:
        # Anything else → show the reason instead of a blank 500
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")