Authentication Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException, status from fastapi.security import OAuth2PasswordRequestForm from core.security import verify_password, get_password_hash, get_current_user, create_access_token from models.user import User from models.loginattempt import LoginAttempt from schemas.user import UserCreate, UserOut, Token from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserOut) async def signup(user_data: UserCreate): existing_user = await User.get_or_none(email=user_data.email) if existing_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

hashed_pw = get_password_hash(user_data.password)
new_user = await User.create(
    email=user_data.email,
    username=user_data.username,
    full_name=user_data.full_name,
    hashed_password=hashed_pw
)
return new_user

@router.post("/login", response_model=Token) async def login(form_data: OAuth2PasswordRequestForm = Depends()): user = await User.get_or_none(email=form_data.username) if not user or not verify_password(form_data.password, user.hashed_password): await LoginAttempt.create(user=user if user else None, status="failed", timestamp=datetime.utcnow()) raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

await LoginAttempt.create(user=user, status="successful", timestamp=datetime.utcnow())

access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=60))
return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut) async def read_users_me(current_user: User = Depends(get_current_user)): return current_user

