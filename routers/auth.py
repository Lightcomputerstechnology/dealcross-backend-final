File: src/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request from fastapi.security import OAuth2PasswordBearer from starlette.responses import JSONResponse from jose import JWTError, jwt from datetime import datetime, timedelta from models.user import User from core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.SECRET_KEY ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

──────────────────── HELPERS ─────────────────────

async def verify_token(token: str) -> User: credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}, ) try: payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) user_id: int = payload.get("user_id") if user_id is None: raise credentials_exception except JWTError: raise credentials_exception

user = await User.get_or_none(id=user_id)
if user is None:
    raise credentials_exception
return user

──────────────────── ROUTES ─────────────────────

@router.get("/me") async def get_current_user(token: str = Depends(oauth2_scheme)) -> User: return await verify_token(token)

@router.post("/verify-email") async def verify_email(token: str): try: payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) user_id: int = payload.get("user_id") if not user_id: raise HTTPException(status_code=400, detail="Invalid token.") except JWTError: raise HTTPException(status_code=400, detail="Invalid or expired token.")

user = await User.get_or_none(id=user_id)
if not user:
    raise HTTPException(status_code=404, detail="User not found.")

if user.email_verified:
    return {"message": "Email already verified."}

user.email_verified = True
await user.save()
return {"message": "Email successfully verified."}

@router.post("/request-verification") async def request_email_verification(request: Request, token: str = Depends(oauth2_scheme)): user = await verify_token(token) if user.email_verified: raise HTTPException(status_code=400, detail="Email is already verified.")

token_data = {
    "user_id": user.id,
    "exp": datetime.utcnow() + timedelta(minutes=30)
}
verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
verify_link = f"https://dealcross.net/verify-email?token={verification_token}"

return JSONResponse(content={"message": "Verification link generated.", "url": verify_link})

