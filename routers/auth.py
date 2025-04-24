from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import (
    verify_password,
    get_password_hash,
    get_current_user,
    create_access_token,
)
from models.user import User
from models.login_attempt import LoginAttempt
from core.database import get_db
from schemas import UserCreate, UserOut
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ───────────────────────────  Sign‑up  ────────────────────────────
@router.post("/signup", response_model=UserOut, summary="Register a new user account")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_pw = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, username=user_data.username, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ───────────────────────────  Login  ──────────────────────────────
@router.post("/login", summary="Authenticate user and log login attempt with token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        db.add(LoginAttempt(user_id=user.id if user else None, status="failed", timestamp=datetime.utcnow()))
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Successful login
    db.add(LoginAttempt(user_id=user.id, status="successful", timestamp=datetime.utcnow()))
    db.commit()

    # Issue JWT token
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

# ───────────────────  Get current user  ────────────────────
@router.get("/me", response_model=UserOut, summary="Retrieve current logged-in user profile")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
