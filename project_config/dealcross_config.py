# File: project_config/dealcross_config.py

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
import logging

logger = logging.getLogger("dealcross.settings")

class Settings(BaseSettings):
    # GENERAL
    APP_NAME: str = Field(..., alias="APP_NAME")
    APP_ENV: str = Field(..., alias="APP_ENV")
    APP_PORT: int = Field(..., alias="APP_PORT")

    # DATABASE
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")

    # SECURITY
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field(..., alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # PAYMENT
    PAYSTACK_SECRET: str = Field(..., alias="PAYSTACK_SECRET")
    FLW_SECRET: str = Field(..., alias="FLW_SECRET")
    NOWPAY_API_KEY: str = Field(..., alias="NOWPAY_API_KEY")

    # EMAIL
    EMAIL_HOST: str = Field(..., alias="EMAIL_HOST")
    EMAIL_PORT: int = Field(587, alias="EMAIL_PORT")
    EMAIL_USER: str = Field(..., alias="EMAIL_USER")
    EMAIL_PASSWORD: str = Field(..., alias="EMAIL_PASSWORD")
    EMAIL_FROM_NAME: str = Field("Dealcross", alias="EMAIL_FROM_NAME")

    # RATE LIMIT
    RATE_LIMIT_MAX_REQUESTS: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    RATE_LIMIT_TIME_WINDOW: int = Field(60, alias="RATE_LIMIT_TIME_WINDOW")

    # FRONTEND
    FRONTEND_URL: str = Field(..., alias="FRONTEND_URL")

    # CALLBACKS
    PAYSTACK_CALLBACK: str = Field(..., alias="PAYSTACK_CALLBACK")
    FLUTTERWAVE_CALLBACK: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    NOWPAY_CALLBACK: str = Field(..., alias="NOWPAY_CALLBACK")

    # REDIS
    REDIS_URL: str = Field(..., alias="REDIS_URL")

    # CONFIGURATION
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

    @model_validator(mode="after")
    def check_critical(self):
        critical_fields = ["DATABASE_URL", "SECRET_KEY", "REDIS_URL"]
        for field in critical_fields:
            if not getattr(self, field, None):
                raise ValueError(f"{field} is required in environment configuration")
        return self

    def get_effective_database_url(self) -> str:
        """Allow future dynamic db switching if needed."""
        return self.DATABASE_URL

# Initialize settings once globally
settings = Settings()

# Structured log confirmation on startup
logger.info("✅ Dealcross settings loaded successfully.")
logger.info(f"✅ REDIS_URL: {settings.REDIS_URL}")