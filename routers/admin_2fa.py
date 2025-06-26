# ======================
# File: routers/admin_2fa.py (Admin 2FA routes)
# ======================
from fastapi import APIRouter, Depends, HTTPException
from utils.twofactor import generate_totp_secret, generate_qr_code, verify_totp
from utils.email_2fa import send_email_otp, verify_email_otp
from models import User
from dependencies import get_current_user  # assume you have this defined

router = APIRouter()

@router.get("/admin/2fa/setup")
async def setup_2fa(current_user: User = Depends(get_current_user)):
    if not current_user.otp_secret:
        current_user.otp_secret = generate_totp_secret()
        await current_user.save()
    return generate_qr_code(current_user.username, current_user.otp_secret)

@router.post("/admin/2fa/verify-totp")
async def verify_totp_code(code: str, current_user: User = Depends(get_current_user)):
    if not verify_totp(current_user.otp_secret, code):
        raise HTTPException(status_code=403, detail="Invalid TOTP code")
    current_user.is_2fa_enabled = True
    await current_user.save()
    return {"detail": "TOTP 2FA enabled successfully"}

@router.post("/admin/2fa/send-email")
async def send_email_code(current_user: User = Depends(get_current_user)):
    await send_email_otp(current_user.email)
    return {"detail": "Verification code sent to your email"}

@router.post("/admin/2fa/verify-email")
async def verify_email_code(code: str, current_user: User = Depends(get_current_user)):
    if not await verify_email_otp(current_user.email, code):
        raise HTTPException(status_code=403, detail="Invalid code")
    current_user.is_2fa_enabled = True
    await current_user.save()
    return {"detail": "Email-based 2FA enabled successfully"}
