from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password, get_password_hash, get_current_user, create_access_token
from models.user import User
from models.login_attempt import LoginAttempt
from schemas.user import UserCreate, UserOut
from schemas.token import Token
from datetime import datetime, timedelta
