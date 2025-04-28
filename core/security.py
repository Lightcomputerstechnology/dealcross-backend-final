from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist
from core.security import verify_password, get_password_hash
from models.user import User
from schemas.user import UserCreate, UserOut
from datetime import datetime, timedelta
