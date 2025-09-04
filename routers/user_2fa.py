from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from core.security import get_current_user  # Supabase-aware claims
from core.settings import settings          # has OTP_ISSUER_NAME via env (fallback handled)
from models.user import User
from utils.otp import generate_totp_secret, generate_totp_uri, verify_totp_code

router = APIRouter(prefix="/user/2fa", tags=["Two-Factor Authentication"])


# Map verified JWT claims -> local DB User
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


@router.post("/enable")
async def enable_2fa(current_user: User = Depends(resolve_db_user)):
    """
    Generate and return TOTP secret & QR URI for the user to enable 2FA.
    """
    if getattr(current_user, "is_2fa_enabled", False):
        raise HTTPException(status_code=400, detail="2FA is already enabled for this account.")

    secret = generate_totp_secret()
    issuer_name = getattr(settings, "otp_issuer_name", None) or getattr(settings, "OTP_ISSUER_NAME", None) or "Dealcross"
    uri = generate_totp_uri(
        user_email=current_user.email,
        secret=secret,
        issuer_name=issuer_name
    )

    current_user.totp_secret = secret
    await current_user.save()

    return {
        "qr_uri": uri,
        "manual_entry_code": secret,
        "message": "Scan the QR code or enter the code in your authenticator app to enable 2FA."
    }


@router.post("/verify")
async def verify_2fa(
    code: str = Query(..., description="The 2FA code from your authenticator app."),
    current_user: User = Depends(resolve_db_user),
):
    """
    Verify the user's 2FA TOTP code and enable 2FA on their account.
    """
    if not getattr(current_user, "totp_secret", None):
        raise HTTPException(status_code=400, detail="No 2FA secret found for this user. Enable 2FA first.")

    if not verify_totp_code(current_user.totp_secret, code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code provided. Please try again.")

    current_user.is_2fa_enabled = True
    await current_user.save()

    return {"message": "✅ Two-Factor Authentication has been enabled successfully for your account."}
