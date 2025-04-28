# File: src/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from tortoise.transactions import in_transaction
from models.user import User
from core.config import settings

router = APIRouter()

# Load secret and algorithm from your config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

async def verify_token(token: str) -> User:
    """
    Verifies a JWT token and returns the corresponding user using Tortoise ORM.
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

async def get_current_user(token: str = Depends(settings.oauth2_scheme)) -> User:
    """
    Dependency to get the current user from the token.
    """
    return await verify_token(token)
