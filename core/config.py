# File: core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ─── SECURITY ───────────────
    SECRET_KEY: str
    ALGORITHM: str

    # ─── DATABASE ───────────────
    DATABASE_URL: str

    # ─── OPTIONAL EMAIL ─────────
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    # ─── OPTIONAL REDIS ─────────
    REDIS_URL: str = ""

    # Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

settings = Settings()