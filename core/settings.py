# core/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ─── General ─────────────────────────────
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # ─── Database ────────────────────────────
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(..., alias="DB_NAME")

    # ─── Security ────────────────────────────
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── Payment Gateway Keys ────────────────
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # ─── Email Config ────────────────────────
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(..., alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field(..., alias="EMAIL_FROM_NAME")

    # ─── Rate Limiting ───────────────────────
    rate_limit_max_requests: int = Field(..., alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(..., alias="RATE_LIMIT_TIME_WINDOW")

    # ─── URLs ────────────────────────────────
    frontend_url: str = Field(..., alias="FRONTEND_URL")
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    class Config:
        env_file = ".env"
        extra = "forbid"  # Disallow undeclared variables


# Create an instance to import elsewhere
settings = Settings()