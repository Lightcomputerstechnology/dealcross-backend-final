from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # GENERAL
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # DATABASE
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(..., alias="DB_NAME")
    db_url: str = Field(None, alias="DATABASE_URL")

    # SECURITY
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # PAYMENTS
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # EMAIL
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(..., alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field(..., alias="EMAIL_FROM_NAME")

    # RATE LIMIT
    rate_limit_max_requests: int = Field(..., alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(..., alias="RATE_LIMIT_TIME_WINDOW")

    # FRONTEND
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    # CALLBACKS
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    # ✅ FIXED: Allow unknown env vars (like in Render)
    class Config:
        extra = "allow"

settings = Settings()