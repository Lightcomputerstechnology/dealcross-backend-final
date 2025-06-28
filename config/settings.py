from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ─── GENERAL ─────────────────────────────
    APP_NAME: str = Field(..., env="APP_NAME")
    APP_ENV: str = Field(..., env="APP_ENV")
    APP_PORT: int = Field(..., env="APP_PORT")

    # ─── DATABASE ────────────────────────────
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_HOST: str = Field(default=None, env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_USER: str = Field(default=None, env="DB_USER")
    DB_PASSWORD: str = Field(default=None, env="DB_PASSWORD")
    DB_NAME: str = Field(default=None, env="DB_NAME")

    # ─── SECURITY ────────────────────────────
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── PAYMENT GATEWAYS ────────────────────
    PAYSTACK_SECRET: str = Field(..., env="PAYSTACK_SECRET")
    FLW_SECRET: str = Field(..., env="FLW_SECRET")
    NOWPAY_API_KEY: str = Field(..., env="NOWPAY_API_KEY")

    # ─── EMAIL CONFIG ────────────────────────
    EMAIL_HOST: str = Field(..., env="EMAIL_HOST")
    EMAIL_PORT: int = Field(default=587, env="EMAIL_PORT")
    EMAIL_USER: str = Field(..., env="EMAIL_USER")
    EMAIL_PASSWORD: str = Field(..., env="EMAIL_PASSWORD")
    EMAIL_FROM_NAME: str = Field(default="Dealcross", env="EMAIL_FROM_NAME")

    # ─── RATE LIMIT ──────────────────────────
    RATE_LIMIT_MAX_REQUESTS: int = Field(default=100, env="RATE_LIMIT_MAX_REQUESTS")
    RATE_LIMIT_TIME_WINDOW: int = Field(default=60, env="RATE_LIMIT_TIME_WINDOW")

    # ─── FRONTEND ────────────────────────────
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")

    # ─── CALLBACKS ───────────────────────────
    PAYSTACK_CALLBACK: str = Field(..., env="PAYSTACK_CALLBACK")
    FLUTTERWAVE_CALLBACK: str = Field(..., env="FLUTTERWAVE_CALLBACK")
    NOWPAY_CALLBACK: str = Field(..., env="NOWPAY_CALLBACK")

    # ─── SETTINGS ────────────────────────────
    class Config:
        env_file = ".env"
        extra = "allow"  # prevents failure if other env vars exist


settings = Settings()