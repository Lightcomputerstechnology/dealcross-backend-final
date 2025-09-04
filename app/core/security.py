# File: app/core/security.py
from typing import Optional, Dict, Any
from functools import lru_cache
from datetime import datetime, timezone

import httpx
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)

class AuthUser(Dict[str, Any]):
    """Light wrapper for user info extracted from Supabase JWT."""

@lru_cache(maxsize=1)
def _jwks() -> Dict[str, Any]:
    if not settings.SUPABASE_JWKS_URL:
        raise RuntimeError("SUPABASE_JWKS_URL not configured")
    with httpx.Client(timeout=5.0) as client:
        resp = client.get(settings.SUPABASE_JWKS_URL)
        resp.raise_for_status()
        return resp.json()

def _decode_with_jwks(token: str) -> Dict[str, Any]:
    # Get unverified header to pick correct key
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    keys = _jwks().get("keys", [])
    public_key = None
    for k in keys:
        if k.get("kid") == kid:
            public_key = k
            break
    if public_key is None:
        raise HTTPException(status_code=401, detail="Invalid token key")

    # Issuer and audience are optional; Supabase signs with its gotrue issuer
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[unverified_header.get("alg", "RS256")],
            options={"verify_aud": False},  # allow any aud (or set your API aud)
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    # Expiry check (defensive)
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired")
    return payload

async def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> AuthUser:
    if not creds or not creds.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = creds.credentials

    # Prefer Supabase JWT via JWKS
    try:
        claims = _decode_with_jwks(token)
        # Normalize common fields for your app
        user_id = claims.get("sub") or claims.get("user_id")  # Supabase uses sub = auth.users.id
        email = (claims.get("email") or claims.get("user_metadata", {}).get("email"))
        user = AuthUser(id=user_id, email=email, claims=claims)
        return user
    except HTTPException:
        # If you still support legacy tokens, you could try decoding with your local secret here:
        # from jose import jwt as jose_jwt
        # try:
        #     payload = jose_jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        #     return AuthUser(id=payload.get("sub"), email=payload.get("email"), claims=payload)
        # except JWTError:
        #     pass
        raise

async def require_admin(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    """
    Admin check:
    - Option A: Frontend checks public.profiles.is_admin directly (recommended)
    - Option B (here): Trust a custom claim if you add it server-side, or
    - Query DB using SUPABASE_SERVICE_ROLE_KEY to check profiles.is_admin
    For now, we support Option B via claim "is_admin" if present; otherwise deny.
    """
    claims = user.get("claims", {})
    is_admin_claim = (
        claims.get("is_admin") or
        claims.get("user_metadata", {}).get("is_admin") or
        False
    )
    if not is_admin_claim:
        # If you prefer a DB check, replace this block with a service-role call to Supabase PostgREST.
        raise HTTPException(status_code=403, detail="Admin access only")
    return user
