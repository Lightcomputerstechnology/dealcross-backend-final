# File: config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # GENERAL
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # DATABASE
    database_url: str = Field(..., alias="DATABASE_URL")
    db_host: str = Field(None, alias="DB_HOST")
    db_port: int = Field(5432, alias="DB_PORT")
    db_user: str = Field(None, alias="DB_USER")
    db_password: str = Field(None, alias="DB_PASSWORD")
    db_name: str = Field(None, alias="DB_NAME")

    # SECURITY
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # PAYMENT GATEWAYS
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

    # REDIS ✅ THIS IS THE CRUCIAL MISSING PIECE
    redis_url: str = Field(..., alias="REDIS_URL")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()