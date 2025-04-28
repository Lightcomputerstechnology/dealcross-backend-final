# File: src/routers/auth.py

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

async def verify_token(token: str) -> User:
    """
    Verifies a JWT token and returns the corresponding user.
    """
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

@router.get("/me", response_model=None)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current user from the token.
    """
    return await verify_token(token)
