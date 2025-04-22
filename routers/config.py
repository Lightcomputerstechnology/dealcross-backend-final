fro# File: routers/config.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import require_admin
from models.config import Config
from schemas.config_schema import ConfigOut
from typing import List

router = APIRouter()

# === Get all settings ===
@router.get("/settings", response_model=List[ConfigOut], tags=["Admin Settings"])
def get_all_settings(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Config).all()

# === Update a setting ===
@router.put("/settings/{key}", response_model=ConfigOut, tags=["Admin Settings"])
def update_setting(
    key: str,
    value: str,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    config = db.query(Config).filter(Config.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Setting not found")

    config.value = value
    db.commit()
    db.refresh(config)
    return config
