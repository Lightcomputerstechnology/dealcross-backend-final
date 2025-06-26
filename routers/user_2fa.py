# routers/user_2fa.py
from fastapi import APIRouter, Depends, HTTPException
from tortoise.transactions import in_transaction
from models.user import User
from utils.otp import generate_totp_secret, get_totp_uri, verify_totp_code
from core.auth import get_current_user  # your custom JWT auth dependency
from config.settings import settings

router = APIRouter(prefix="/user/2fa", tags=["Two-Factor"])

@router.post("/enable")
async def enable_2fa(current_user: User = Depends(get_current_user)):
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled.")

    secret = generate_totp_secret()
    uri = get_totp_uri(current_user, secret, settings.OTP_ISSUER_NAME)

    # Save temporary secret for verification
    current_user.totp_secret = secret
    await current_user.save()

    return {
        "qr_uri": uri,
        "manual_entry_code": secret
    }

@router.post("/verify")
async def verify_2fa(code: str, current_user: User = Depends(get_current_user)):
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="No secret found.")

    if not verify_totp_code(current_user.totp_secret, code):
        raise HTTPException(status_code=400, detail="Invalid code.")

    current_user.is_2fa_enabled = True
    await current_user.save()
    return {"message": "2FA enabled successfully."}