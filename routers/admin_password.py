# File: routers/admin_password.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from tortoise.transactions import in_transaction
from passlib.context import CryptContext
from core.security import get_current_user
from models.user import User

router = APIRouter(tags=["Admin Tools"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/admin/change-password")
async def change_admin_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access denied.")

    if not pwd_context.verify(payload.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect current password.")

    hashed = pwd_context.hash(payload.new_password)

    async with in_transaction():
        current_user.password = hashed
        await current_user.save()

    return {"message": "Password changed successfully."}