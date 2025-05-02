# File: core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str

    # SMTP Settings
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()