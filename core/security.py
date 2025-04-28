# core/security.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# OAuth2 scheme (example setup)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# You can add additional authentication utilities here...
