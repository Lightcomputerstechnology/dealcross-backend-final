from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User
from core.config import settings

# Initialize FastAPI APIRouter
router = APIRouter(prefix="/auth", tags=["Auth"])

# Load secret and algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# Setup OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# === Helper to verify token and get user ===
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

# === GET current user from token ===
@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await verify_token(token)

# === GET /auth/verify-email?token=XYZ123 ===
@router.get("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.email_verified:
            return {"message": "Email already verified."}

        user.email_verified = True
        await user.save()

        return {"message": "Email verification successful."}

    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")