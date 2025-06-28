import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # ─── GENERAL ─────────────────────────────
    APP_NAME: str = "Dealcross"
    APP_ENV: str = "production"
    APP_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "info"
    TIMEZONE: str = "UTC"

    # ─── DATABASE ────────────────────────────
    DATABASE_URL: str

    # ─── SECURITY ────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ─── PAYMENT API KEYS ────────────────────
    PAYSTACK_SECRET: str
    FLW_SECRET: str
    NOWPAY_API_KEY: str

    # ─── EMAIL SMTP ──────────────────────────
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM_NAME: str

    # ─── RATE LIMITING ───────────────────────
    RATE_LIMIT_MAX_REQUESTS: int = 100
    RATE_LIMIT_TIME_WINDOW: int = 60

    # ─── FRONTEND ────────────────────────────
    FRONTEND_URL: str

    # ─── CALLBACK / WEBHOOK URLs ─────────────
    PAYSTACK_CALLBACK: str
    FLUTTERWAVE_CALLBACK: str
    NOWPAY_CALLBACK: str

    # ─── MONITORING & ANALYTICS ──────────────
    SENTRY_DSN: Optional[str] = None
    GOOGLE_ANALYTICS_ID: Optional[str] = None

    # ─── EMAIL TEMPLATES (OPTIONAL) ──────────
    EMAIL_VERIFICATION_TEMPLATE: Optional[str] = "email/verify.html"
    PASSWORD_RESET_TEMPLATE: Optional[str] = "email/reset.html"
    KYC_APPROVAL_TEMPLATE: Optional[str] = "email/kyc_approved.html"

    # ─── TWO-FACTOR AUTH ─────────────────────
    ENABLE_2FA: bool = True
    OTP_ISSUER_NAME: Optional[str] = "Dealcross"
    OTP_EMAIL_TEMPLATE: Optional[str] = "email/otp_code.html"

    # ─── REDIS ───────────────────────────────
    REDIS_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"

settings = Settings()