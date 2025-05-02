# File: core/config.py

from pydantic_settings import BaseSettings  # You can also use 'from pydantic import BaseSettings' if pydantic v1
# If you face issues with pydantic_settings, fallback to: from pydantic import BaseSettings

class Settings(BaseSettings):
    # JWT Authentication Settings
    SECRET_KEY: str = "YOUR_SECRET_KEY"  # Replace with a secure key!
    ALGORITHM: str = "HS256"

    # Database (loaded from .env)
    DATABASE_URL: str

    # Email / SMTP Settings
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    class Config:
        env_file = ".env"  # This tells Pydantic to load variables from .env

# Global settings instance to be imported everywhere
settings = Settings()