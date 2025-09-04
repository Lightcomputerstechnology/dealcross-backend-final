from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException

from core.security import get_current_user            # Supabase-aware claims
from core.supabase_client import get_profile_is_admin # server-side admin check

from models.config import Config
from schemas.config_schema import ConfigOut

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


# Map verified JWT claims → local DB User (email only; we don't need full row here)
async def _claims(claims: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    if not claims.get("email"):
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    return claims

# Admin guard (Supabase profiles.is_admin or local override via role/is_admin on user if you later add it)
async def _require_admin(claims: Dict[str, Any] = Depends(_claims)) -> None:
    supa_user_id = claims.get("sub")
    if not supa_user_id or not get_profile_is_admin(supa_user_id):
        # If you also want local fallback, replace this with the shared require_admin used elsewhere
        raise HTTPException(status_code=403, detail="Admin access only.")


# === Get all settings ===
@router.get("/", response_model=List[ConfigOut])
async def get_all_settings(_: None = Depends(_require_admin)):
    items = await Config.all().order_by("key")
    return [await ConfigOut.from_tortoise_orm(c) for c in items]


# === Update a setting ===
@router.put("/{key}", response_model=ConfigOut)
async def update_setting(key: str, value: str, _: None = Depends(_require_admin)):
    config = await Config.get_or_none(key=key)
    if not config:
        raise HTTPException(status_code=404, detail="Setting not found")

    config.value = value
    await config.save()
    return await ConfigOut.from_tortoise_orm(config)
```0
