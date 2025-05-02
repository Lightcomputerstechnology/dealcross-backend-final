# File: core/config.py

from pydantic_settings import BaseSettings  # or fallback to 'from pydantic import BaseSettings'

class Settings(BaseSettings):
    # JWT Authentication Settings
    SECRET_KEY: str
    ALGORITHM: str

    # Database
    DATABASE_URL: str

    # Email / SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    class Config:
        env_file = ".env"
        extra = "ignore"  # ✅ This prevents crashes from unknown environment vars

# Global config instance
settings = Settings()