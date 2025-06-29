# File: core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ─── GENERAL ─────────────────────────────
    APP_NAME: str
    APP_ENV: str
    APP_PORT: int

    # ─── DATABASE ────────────────────────────
    DATABASE_URL: str

    # ─── SECURITY ────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ─── REDIS ───────────────────────────────
    REDIS_URL: str

    # ─── OPTIONAL EMAIL ──────────────────────
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()