# File: core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Core Auth Settings
    SECRET_KEY: str
    ALGORITHM: str

    # DB Settings
    DATABASE_URL: str

    # Optional Email Configs
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    # Redis (Optional)
    REDIS_URL: str = ""  # or without default if mandatory

    # Pydantic v2 compatible config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

settings = Settings()