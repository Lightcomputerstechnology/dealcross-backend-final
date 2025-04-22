# utils/auth.py

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from core.config import settings  # Assuming you have a central config file for SECRET_KEY, etc.

# Load secret and algorithm from your config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def verify_token(token: str, db: Session) -> User:
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

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    """
    Dependency to get the current user from the token.
    """
    return verify_token(token, db)
