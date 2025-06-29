# File: project_config/dealcross_config.py

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
import logging

logger = logging.getLogger("dealcross.settings")

class Settings(BaseSettings):
    # GENERAL
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # DATABASE
    database_url: str = Field(..., alias="DATABASE_URL")

    # SECURITY
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # PAYMENT
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # EMAIL
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(587, alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field("Dealcross", alias="EMAIL_FROM_NAME")

    # RATE LIMIT
    rate_limit_max_requests: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(60, alias="RATE_LIMIT_TIME_WINDOW")

    # FRONTEND
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    # CALLBACKS
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    # REDIS
    redis_url: str = Field(..., alias="REDIS_URL")

    # CONFIGURATION
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

    @model_validator(mode="after")
    def check_critical(self):
        critical_fields = ["database_url", "secret_key", "redis_url"]
        for field in critical_fields:
            if not getattr(self, field, None):
                raise ValueError(f"{field} is required in environment configuration")
        return self

    def get_effective_database_url(self) -> str:
        """Allow future dynamic db switching if needed."""
        return self.database_url

# Initialize settings once globally
settings = Settings()

# Structured log confirmation on startup
logger.info("✅ Dealcross settings loaded successfully.")
logger.info(f"✅ REDIS_URL: {settings.redis_url}")