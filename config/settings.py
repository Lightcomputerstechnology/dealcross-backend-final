# config/settings.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env
env_path = Path(__file__).parent.parent / '.env'
print(f"Loading .env from: {env_path.resolve()}")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    DATABASE_URL: str | None = None
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""

    REDIS_URL: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"

    def get_effective_database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if self.DB_USER and self.DB_PASSWORD and self.DB_HOST and self.DB_NAME:
            return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        raise ValueError("DATABASE_URL is not set and DB connection parts are incomplete.")

settings = Settings()

# Debug dump
print("[DEBUG] settings.DATABASE_URL:", settings.DATABASE_URL)
print("[DEBUG] settings.get_effective_database_url:", settings.get_effective_database_url())
print("[DEBUG] settings.SECRET_KEY:", settings.SECRET_KEY)
print("[DEBUG] settings.REDIS_URL:", settings.REDIS_URL)