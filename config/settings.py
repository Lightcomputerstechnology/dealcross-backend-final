# File: config/settings.py

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

# Optional: debug print during container startup
print("🔍 Loading settings from .env")

class Settings(BaseSettings):
    # ─── GENERAL ─────────────────────────────
    app_name: str = Field("Dealcross", alias="APP_NAME")
    app_env: str = Field("production", alias="APP_ENV")
    app_port: int = Field(8000, alias="APP_PORT")
    debug: bool = Field(False, alias="DEBUG")
    log_level: str = Field("info", alias="LOG_LEVEL")
    timezone: str = Field("UTC", alias="TIMEZONE")

    # ─── DATABASE ────────────────────────────
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(..., alias="DB_NAME")
    database_url: str = Field(..., alias="DATABASE_URL")

    # ─── SECURITY ────────────────────────────
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── PAYMENT API KEYS ────────────────────
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flutterwave_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # ─── EMAIL SMTP ──────────────────────────
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(..., alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field(..., alias="EMAIL_FROM_NAME")

    # ─── RATE LIMITING ───────────────────────
    rate_limit_max_requests: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(60, alias="RATE_LIMIT_TIME_WINDOW")

    # ─── FRONTEND ────────────────────────────
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    # ─── CALLBACK / WEBHOOK URLs ─────────────
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    # ─── MONITORING & ANALYTICS ──────────────
    sentry_dsn: Optional[str] = Field(None, alias="SENTRY_DSN")
    google_analytics_id: Optional[str] = Field(None, alias="GOOGLE_ANALYTICS_ID")

    # ─── EMAIL TEMPLATES ─────────────────────
    email_verification_template: Optional[str] = Field("email/verify.html", alias="EMAIL_VERIFICATION_TEMPLATE")
    password_reset_template: Optional[str] = Field("email/reset.html", alias="PASSWORD_RESET_TEMPLATE")
    kyc_approval_template: Optional[str] = Field("email/kyc_approved.html", alias="KYC_APPROVAL_TEMPLATE")

    # ─── TWO-FACTOR AUTH ─────────────────────
    enable_2fa: bool = Field(True, alias="ENABLE_2FA")
    otp_issuer_name: Optional[str] = Field("Dealcross", alias="OTP_ISSUER_NAME")
    otp_email_template: Optional[str] = Field("email/otp_code.html", alias="OTP_EMAIL_TEMPLATE")

    # ─── REDIS CONFIG ────────────────────────
    redis_url: str = Field(..., alias="REDIS_URL")

    # ─── TORTOISE ORM (Optional) ─────────────
    tortoise_orm: Optional[str] = Field(None, alias="TORTOISE_ORM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # ignores extra unexpected env vars safely

# Instantiate globally for imports
settings = Settings()

# Debug confirmation
print(f"✅ Loaded settings: environment={settings.app_env}, db_url={settings.database_url}, redis_url={settings.redis_url}")