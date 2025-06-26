# File: core/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Only the environment variables your app depends on
    app_name: str = Field(..., alias="APP_NAME")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")

    # Payment Gateways
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    class Config:
        extra = "allow"  # ✅ Prevents Pydantic from crashing on undeclared env vars

# Global instance to import anywhere
settings = Settings()