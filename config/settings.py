import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # General
    app_name: str = Field("Dealcross", alias="APP_NAME")
    app_env: str = Field("production", alias="APP_ENV")
    app_port: int = Field(8000, alias="APP_PORT")
    debug: bool = Field(False, alias="DEBUG")
    log_level: str = Field("info", alias="LOG_LEVEL")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")

    # Security
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")

    # Redis
    redis_url: str = Field(..., alias="REDIS_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Optional debug confirmation
print("[Settings] Loaded DATABASE_URL:", settings.database_url)
print("[Settings] Loaded REDIS_URL:", settings.redis_url)
