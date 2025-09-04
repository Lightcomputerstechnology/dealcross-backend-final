# core/supabase_client.py
from __future__ import annotations
import os
import httpx

# We use SERVICE ROLE to read public.profiles securely on the server.
SUPABASE_URL = os.getenv("SUPABASE_URL") or ""
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE") or ""

def _headers():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE in environment.")
    return {"Authorization": f"Bearer {SUPABASE_SERVICE_ROLE}", "apikey": SUPABASE_SERVICE_ROLE}

def get_profile_is_admin(auth_user_id: str) -> bool | None:
    """
    Returns True/False if the row exists and has is_admin set,
    or None if no matching profile was found.
    Expects a table `public.profiles` with columns:
      - auth_user_id (uuid, references auth.users.id)
      - is_admin (boolean)
    """
    url = f"{SUPABASE_URL}/rest/v1/profiles"
    params = {
        "select": "is_admin",
        "auth_user_id": f"eq.{auth_user_id}",
        "limit": 1
    }
    with httpx.Client(timeout=5.0) as client:
        resp = client.get(url, headers=_headers(), params=params)
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            return None
        row = rows[0]
        return bool(row.get("is_admin"))
