Config Settings Router (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from core.dependencies import require_admin from models.config import Config from schemas.config_schema import ConfigOut from typing import List

router = APIRouter()

=== Get all settings ===

@router.get("/settings", response_model=List[ConfigOut], tags=["Admin Settings"]) async def get_all_settings(admin=Depends(require_admin)): return await Config.all()

=== Update a setting ===

@router.put("/settings/{key}", response_model=ConfigOut, tags=["Admin Settings"]) async def update_setting( key: str, value: str, admin=Depends(require_admin) ): config = await Config.get_or_none(key=key) if not config: raise HTTPException(status_code=404, detail="Setting not found")

config.value = value
await config.save()
return config

