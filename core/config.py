# File: core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field(..., alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    REDIS_URL: str = Field("", alias="REDIS_URL")

    SMTP_SERVER: str = Field("", alias="SMTP_SERVER")
    SMTP_PORT: int = Field(587, alias="SMTP_PORT")
    SMTP_USERNAME: str = Field("", alias="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field("", alias="SMTP_PASSWORD")
    SMTP_FROM: str = Field("", alias="SMTP_FROM")

    APP_NAME: str = Field("", alias="APP_NAME")
    APP_ENV: str = Field("", alias="APP_ENV")
    APP_PORT: int = Field(8000, alias="APP_PORT")

    class Config:
        env_file = ".env"
        extra = "allow"
        allow_population_by_field_name = True  # ✅ allow usage by field name if ever needed

settings = Settings()
