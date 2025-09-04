from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user                 # Supabase-aware claims (JWKS-verified)
from core.supabase_client import get_profile_is_admin      # server-side admin check (SERVICE ROLE)
from models.user import User
from utils.twofactor import generate_totp_secret, generate_qr_code, verify_totp
from utils.email_2fa import send_email_otp, verify_email_otp

router = APIRouter(prefix="/admin/2fa", tags=["Admin 2FA"])


# ─────────── Helpers: claims → DB user + admin guard ───────────

async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user

async def require_admin(
    claims: Dict[str, Any] = Depends(get_current_user),
    db_user: User = Depends(resolve_db_user),
) -> User:
    # Prefer Supabase profiles.is_admin; fall back to local role/is_admin if present
    supa_user_id = claims.get("sub")
    is_admin = bool(supa_user_id and get_profile_is_admin(supa_user_id))
    if not is_admin and (getattr(db_user, "is_admin", False) or getattr(db_user, "role", "") == "admin"):
        is_admin = True
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access only.")
    return db_user


# ─────────── Field accessors for otp/totp secret (support both names) ───────────

def _get_secret_attr_name(user: User) -> str:
    # Prefer `totp_secret` (used elsewhere), but support `otp_secret`
    if hasattr(user, "totp_secret"):
        return "totp_secret"
    if hasattr(user, "otp_secret"):
        return "otp_secret"
    # If neither exists, default to `totp_secret` (Tortoise will error if model truly lacks it)
    return "totp_secret"


# ─────────── Routes ───────────

@router.get("/setup")
async def setup_2fa(admin_user: User = Depends(require_admin)):
    """
    Generate (if missing) a TOTP secret and return a QR representation for admin.
    """
    secret_field = _get_secret_attr_name(admin_user)
    secret_val = getattr(admin_user, secret_field, None)

    if not secret_val:
        secret_val = generate_totp_secret()
        setattr(admin_user, secret_field, secret_val)
        await admin_user.save()

    # Use username if present; else fall back to email
    label = getattr(admin_user, "username", None) or getattr(admin_user, "email", "admin@dealcross")
    return generate_qr_code(label, secret_val)


@router.post("/verify-totp")
async def verify_totp_code(code: str, admin_user: User = Depends(require_admin)):
    """
    Verify TOTP and mark admin 2FA as enabled.
    """
    secret_field = _get_secret_attr_name(admin_user)
    secret_val = getattr(admin_user, secret_field, None)
    if not secret_val:
        raise HTTPException(status_code=400, detail="No TOTP secret set. Run setup first.")

    if not verify_totp(secret_val, code):
        raise HTTPException(status_code=403, detail="Invalid TOTP code")

    # Support either boolean field name
    if hasattr(admin_user, "is_2fa_enabled"):
        admin_user.is_2fa_enabled = True
    elif hasattr(admin_user, "twofa_enabled"):
        admin_user.twofa_enabled = True
    else:
        # Default to is_2fa_enabled if schema is uncertain
        setattr(admin_user, "is_2fa_enabled", True)

    await admin_user.save()
    return {"detail": "TOTP 2FA enabled successfully"}


@router.post("/send-email")
async def send_email_code(admin_user: User = Depends(require_admin)):
    """
    Send OTP to admin's email for email-based 2FA.
    """
    email = getattr(admin_user, "email", None)
    if not email:
        raise HTTPException(status_code=400, detail="Admin account has no email")
    await send_email_otp(email)
    return {"detail": "Verification code sent to your email"}


@router.post("/verify-email")
async def verify_email_code(code: str, admin_user: User = Depends(require_admin)):
    """
    Verify email OTP and mark admin 2FA as enabled.
    """
    email = getattr(admin_user, "email", None)
    if not email:
        raise HTTPException(status_code=400, detail="Admin account has no email")

    ok = await verify_email_otp(email, code)
    if not ok:
        raise HTTPException(status_code=403, detail="Invalid code")

    # Support either boolean field name
    if hasattr(admin_user, "is_2fa_enabled"):
        admin_user.is_2fa_enabled = True
    elif hasattr(admin_user, "twofa_enabled"):
        admin_user.twofa_enabled = True
    else:
        setattr(admin_user, "is_2fa_enabled", True)

    await admin_user.save()
    return {"detail": "Email-based 2FA enabled successfully"}
