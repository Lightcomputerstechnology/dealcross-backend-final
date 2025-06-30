# File: core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # ─── GENERAL ─────────────────────────────
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # ─── DATABASE ────────────────────────────
    database_url: str = Field(..., alias="DATABASE_URL")

    # ─── SECURITY ────────────────────────────
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── REDIS ───────────────────────────────
    redis_url: str = Field(..., alias="REDIS_URL")

    # ─── OPTIONAL EMAIL ──────────────────────
    smtp_server: str = Field("", alias="SMTP_SERVER")
    smtp_port: int = Field(587, alias="SMTP_PORT")
    smtp_username: str = Field("", alias="SMTP_USERNAME")
    smtp_password: str = Field("", alias="SMTP_PASSWORD")
    smtp_from: str = Field("", alias="SMTP_FROM")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

settings = Settings()

# ─── TORTOISE ORM CONFIGURATION FOR AERICH ─────────────
TORTOISE_ORM = {
    "connections": {
        "default": settings.database_url,
    },
    "apps": {
        "models": {
            "models": [
                "models",               # ✅ load all your models automatically if __all__ used
                "aerich.models"         # ✅ needed for migrations
            ],
            "default_connection": "default",
        }
    }
}