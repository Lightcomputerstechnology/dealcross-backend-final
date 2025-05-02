# File: core/config.py

from pydantic_settings import BaseSettings  # For pydantic v2
# If pydantic v1, change to: from pydantic import BaseSettings

class Settings(BaseSettings):
    # Auth & security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str

    # Email / SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    model_config = {
        "env_file": ".env",
        "extra": "allow"  # Optional: allow future keys without breaking
    }

settings = Settings()