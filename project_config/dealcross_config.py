# File: project_config/dealcross_config.py

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
import logging

logger = logging.getLogger("dealcross.settings")
logging.basicConfig(level=logging.INFO)

class DealcrossSettings(BaseSettings):
    """
    DealcrossSettings handles environment configuration
    using pydantic_settings for type-safe .env loading.
    """

    # ─── GENERAL ─────────────────────────────
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # ─── DATABASE CONFIG ─────────────────────
    database_url: str = Field(..., alias="DATABASE_URL")

    # ─── SECURITY KEYS ───────────────────────
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── PAYMENT GATEWAYS ────────────────────
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # ─── EMAIL SENDER ────────────────────────
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(587, alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field("Dealcross", alias="EMAIL_FROM_NAME")

    # ─── RATE LIMIT ──────────────────────────
    rate_limit_max_requests: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(60, alias="RATE_LIMIT_TIME_WINDOW")

    # ─── FRONTEND DOMAIN ─────────────────────
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    # ─── CALLBACK/WEBHOOK URLs ───────────────
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    # ─── REDIS URL ───────────────────────────
    redis_url: str = Field(..., alias="REDIS_URL")

    # ─── CONFIGURATION ───────────────────────
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

    @model_validator(mode="after")
    def check_critical(self):
        """
        Validates critical environment configurations are present.
        """
        critical_fields = ["database_url", "jwt_secret", "redis_url"]
        for field in critical_fields:
            if not getattr(self, field, None):
                raise ValueError(f"{field} is required in environment configuration")
        return self

    def get_effective_database_url(self) -> str:
        """
        Returns the effective database URL for Tortoise ORM.
        Handles scheme correction if needed.
        """
        url = self.database_url
        if url.startswith("postgresql://"):
            # Tortoise requires 'postgres://' instead of 'postgresql://'
            return url.replace("postgresql://", "postgres://", 1)
        return url

# ✅ Instantiate global settings for app-wide usage
settings = DealcrossSettings()

# ✅ Logging for debugging
logger.info("✅ Dealcross settings loaded successfully.")
logger.info(f"✅ REDIS_URL: {settings.redis_url}")
logger.info(f"✅ DATABASE_URL (effective): {settings.get_effective_database_url()}")