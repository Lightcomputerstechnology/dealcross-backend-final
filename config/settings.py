# config/settings.py

from pydantic_settings import BaseSettings  # or: from pydantic import BaseSettings for pydantic v1
from dotenv import load_dotenv
import os

# Force load .env explicitly from project root
load_dotenv(".env")

class Settings(BaseSettings):
    # Core Auth Settings
    SECRET_KEY: str
    ALGORITHM: str

    # DB Settings
    DATABASE_URL: str | None = None
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""

    # Optional Email Configs
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    # Redis
    REDIS_URL: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def effective_database_url(self):
        # Allow fallback if DATABASE_URL is empty
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if self.DB_USER and self.DB_PASSWORD and self.DB_HOST and self.DB_NAME:
            return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        raise ValueError("DATABASE_URL is not set and DB connection parts are incomplete.")

# Instantiate the settings for global use
settings = Settings()