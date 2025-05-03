# File: src/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.user import User
from schemas.user_schema import UserOut, UserCreate  # At the top
from core.config import settings
from core.security import get_password_hash
import random, string

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
    # Check if user already exists
    existing = await User.get_or_none(email=user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Handle optional referrer
    referrer = None
    if user_data.referrer_code:
        referrer = await User.get_or_none(referral_code=user_data.referrer_code)
        if not referrer:
            raise HTTPException(status_code=400, detail="Invalid referrer code.")

    # Generate unique referral code
    code_exists = True
    while code_exists:
        generated_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        code_exists = await User.exists(referral_code=generated_code)

    # Create user
    new_user = await User.create(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        referral_code=generated_code,
        referred_by=referrer,
    )

    return {"message": "Signup successful", "user_id": new_user.id, "referral_code": new_user.referral_code}

@router.get("/me", response_model=UserOut)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    return user

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
async def request_email_verification(
    request: Request,
    token: str = Depends(oauth2_scheme)
):
    user = await verify_token(token)
    if user.email_verified:
        raise HTTPException(status_code=400, detail="Email is already verified.")

    token_data = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verify_link = f"https://dealcross.net/verify-email?token={verification_token}"

    return JSONResponse(content={"message": "Verification link generated.", "url": verify_link})
        
