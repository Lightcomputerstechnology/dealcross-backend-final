# routers/auth.py   (top of file)

from fastapi import APIRouter, Depends, HTTPException, status
...
router = APIRouter(          # ← rename from authrouter  →  router
    prefix="/auth",
    tags=["Authentication"]
)

# and everywhere below:
@router.post("/signup",  ...)     # not @authrouter.post(...)
@router.post("/login",   ...)
@router.get ("/me",      ...)
