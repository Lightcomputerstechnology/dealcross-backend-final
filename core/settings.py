from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(..., alias="APP_NAME")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")

    # Optional: only include the keys you're actually using
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    class Config:
        env_file = None           # ✅ disables .env loading
        extra = "ignore"          # ✅ ignores extra keys from Render

# Global settings instance
settings = Settings()