# core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Authentication Settings
    SECRET_KEY: str = "YOUR_SECRET_KEY"  # Replace with a secure key!
    ALGORITHM: str = "HS256"

    # Database (already present)
    DATABASE_URL: str = ""

    # Email / SMTP (already present)
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    # Other configs (add as needed)

settings = Settings()
