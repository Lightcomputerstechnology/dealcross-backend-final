# core/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # ─── GENERAL ───────────────
    APP_NAME: str = "Dealcross"
    APP_ENV: str = "production"
    APP_PORT: int = 8000

    # ─── DATABASE ──────────────
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # ─── SECURITY ──────────────
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ─── PAYMENT KEYS ──────────
    PAYSTACK_SECRET: str
    FLW_SECRET: str
    NOWPAY_API_KEY: str

    # ─── EMAIL (Optional) ──────
    EMAIL_HOST: str | None = None
    EMAIL_PORT: int | None = None
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None
    EMAIL_FROM_NAME: str | None = None

    # ─── RATE LIMIT ────────────
    RATE_LIMIT_MAX_REQUESTS: int = 100
    RATE_LIMIT_TIME_WINDOW: int = 60

    # ─── FRONTEND DOMAIN ───────
    FRONTEND_URL: str

    # ─── CALLBACK URLS ─────────
    PAYSTACK_CALLBACK: str
    FLUTTERWAVE_CALLBACK: str
    NOWPAY_CALLBACK: str

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env")

# Global instance
settings = Settings()