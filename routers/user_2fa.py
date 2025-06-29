# File: routers/user_2fa.py

from fastapi import APIRouter, Depends, HTTPException, Query
from models.user import User
from utils.otp import generate_totp_secret, get_totp_uri, verify_totp_code
from core.auth import get_current_user
from project_config.dealcross_config import settings  # ✅ Updated import path

router = APIRouter(prefix="/user/2fa", tags=["Two-Factor Authentication"])

@router.post("/enable")
async def enable_2fa(current_user: User = Depends(get_current_user)):
    """
    Generate and return TOTP secret & QR URI for the user to enable 2FA.
    """
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled.")

    secret = generate_totp_secret()
    uri = get_totp_uri(
        user_email=current_user.email,
        secret=secret,
        issuer_name=settings.otp_issuer_name  # ✅ Lowercase attribute
    )

    current_user.totp_secret = secret
    await current_user.save()

    return {
        "qr_uri": uri,
        "manual_entry_code": secret
    }

@router.post("/verify")
async def verify_2fa(
    code: str = Query(..., description="The 2FA code from your authenticator app."),
    current_user: User = Depends(get_current_user)
):
    """
    Verify the user's 2FA TOTP code and enable 2FA on their account.
    """
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="No 2FA secret found for this user.")

    if not verify_totp_code(current_user.totp_secret, code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code provided.")

    current_user.is_2fa_enabled = True
    await current_user.save()

    return {"message": "2FA enabled successfully for your account."}