# File: core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from urllib.parse import urlparse

class Settings(BaseSettings):
    # General
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # Security
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")

    # Redis
    redis_url: str = Field(..., alias="REDIS_URL")

    # Config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

    @field_validator("database_url", mode="before")
    def ensure_postgres_scheme(cls, v):
        if v.startswith("postgresql://"):
            # Convert to postgres:// for Tortoise compatibility
            return v.replace("postgresql://", "postgres://", 1)
        return v

settings = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": settings.database_url,
    },
    "apps": {
        "models": {
            "models": [
                "models",         # Auto-discovers models with __all__
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}