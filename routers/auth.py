# File: src/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.user import User
from schemas.user_schema import UserOut, UserCreate
from core.config import settings
from core.security import get_password_hash, verify_password, create_access_token
from utils.otp import verify_totp_code, generate_totp_uri, generate_totp_secret
from utils.email_otp import send_email_otp
import random, string, secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ FIXED: Use exact casing from Pydantic Settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Temporary in-memory pending 2FA session store (replace with Redis in production)
pending_2fa_sessions = {}

# ────────── HELPERS ──────────

async def verify_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get_or_none(id=user_id)
    if user is None:
        raise credentials_exception
    return user

# ────────── ROUTES ──────────

@router.post("/signup", summary="Register a new user")
async def signup(user_data: UserCreate):
    existing = await User.get_or_none(email=user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    referrer = None
    if user_data.referrer_code:
        referrer = await User.get_or_none(referral_code=user_data.referrer_code)
        if not referrer:
            raise HTTPException(status_code=400, detail="Invalid referrer code.")

    code_exists = True
    while code_exists:
        generated_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        code_exists = await User.exists(referral_code=generated_code)

    new_user = await User.create(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        referral_code=generated_code,
        referred_by=referrer,
    )

    return {"message": "Signup successful", "user_id": new_user.id, "referral_code": new_user.referral_code}

@router.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    user = await User.get_or_none(username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if user.is_2fa_enabled:
        session_token = secrets.token_hex(16)
        pending_2fa_sessions[session_token] = user.id
        return {"2fa_required": True, "session_token": session_token}

    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/2fa-login")
async def two_factor_login(session_token: str = Body(...), code: str = Body(...)):
    user_id = pending_2fa_sessions.get(session_token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired session.")

    user = await User.get_or_none(id=user_id)
    if not user or not verify_totp_code(user.totp_secret, code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code.")

    del pending_2fa_sessions[session_token]
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/enable-2fa")
async def enable_2fa(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled.")

    totp_secret = generate_totp_secret()
    user.totp_secret = totp_secret
    await user.save()

    uri = generate_totp_uri(user.username, totp_secret, issuer="Dealcross")
    return {"message": "2FA setup initiated.", "otp_uri": uri}

@router.post("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.email_verified:
        return {"message": "Email already verified."}

    user.email_verified = True
    await user.save()
    return {"message": "Email successfully verified."}

@router.post("/request-verification")
async def request_email_verification(request: Request, token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if user.email_verified:
        raise HTTPException(status_code=400, detail="Email is already verified.")

    token_data = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)}
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verify_link = f"https://dealcross.net/verify-email?token={verification_token}"

    return JSONResponse(content={"message": "Verification link generated.", "url": verify_link})

@router.post("/request-email-otp")
async def request_email_otp(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    await send_email_otp(user)
    return {"message": "OTP sent to your email."}

@router.post("/email-otp-login")
async def email_otp_login(username: str = Body(...), otp: str = Body(...)):
    user = await User.get_or_none(username=username)
    if not user or user.otp_code != otp or user.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    user.otp_code = None
    user.otp_expiry = None
    await user.save()

    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    return user