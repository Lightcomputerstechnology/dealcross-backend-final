# File: core/security.py

from __future__ import annotations

from functools import lru_cache
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from core.settings import settings  # expects SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SUPABASE_JWKS_URL

# ───────────────── OAuth2 (legacy token endpoint used by your existing flow) ─────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ───────────────── Password hashing (kept for legacy/local accounts) ─────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ───────────────── Legacy JWT helpers (HS256 with local SECRET_KEY) ─────────────────
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_legacy_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# ───────────────── Supabase JWT (RS256 via JWKS) ─────────────────
@lru_cache(maxsize=1)
def _get_jwks() -> Dict[str, Any]:
    """Fetch and cache Supabase JWKS once. Requires SUPABASE_JWKS_URL in settings."""
    jwks_url = getattr(settings, "SUPABASE_JWKS_URL", None)
    if not jwks_url:
        raise RuntimeError("SUPABASE_JWKS_URL is not configured in settings.")
    with httpx.Client(timeout=5.0) as client:
        resp = client.get(jwks_url)
        resp.raise_for_status()
        return resp.json()

def decode_supabase_token(token: str) -> dict:
    """
    Decode and verify a Supabase JWT using JWKS. Raises HTTPException on failure.
    """
    try:
        unverified = jwt.get_unverified_header(token)
        kid = unverified.get("kid")
        alg = unverified.get("alg", "RS256")

        keys = _get_jwks().get("keys", [])
        public_key: Optional[Dict[str, Any]] = next((k for k in keys if k.get("kid") == kid), None)
        if not public_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token key")

        payload = jwt.decode(
            token,
            public_key,           # jose accepts a JWK dict
            algorithms=[alg],
            options={"verify_aud": False},  # set to True and supply audience if you enforce aud
        )

        # Defensive exp check (jose already checks if 'exp' present)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")

# ───────────────── Unified dependency used by routers ─────────────────
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Preferred: verify Supabase JWT via JWKS (if configured).
    Fallback: verify legacy HS256 token with local SECRET_KEY.

    Returns the decoded JWT payload dict on success.
    """
    # Try Supabase first when configured
    if getattr(settings, "SUPABASE_JWKS_URL", None):
        try:
            claims = decode_supabase_token(token)
            # Normalize a few common fields for convenience
            # Supabase uses 'sub' = auth.users.id; email may be under 'email' or user_metadata.email
            claims.setdefault("sub", claims.get("user_id") or claims.get("sub"))
            claims.setdefault("email", claims.get("email") or (claims.get("user_metadata") or {}).get("email"))
            claims["auth_source"] = "supabase"
            return claims
        except HTTPException:
            # Fall through to legacy if Supabase verification fails
            pass

    # Legacy fallback (HS256)
    user = decode_legacy_token(token)
    if user:
        user["auth_source"] = "legacy"
        return user

    # If neither worked, deny
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
```0
