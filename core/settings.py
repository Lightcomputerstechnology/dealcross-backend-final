# File: core/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field
import logging

# Logger for clear structured deployment visibility
logger = logging.getLogger("dealcross.settings")
logging.basicConfig(level=logging.INFO)

class Settings(BaseSettings):
    """
    Lightweight but complete settings for shared imports across the entire project.
    Load environment variables consistently using Pydantic.
    """

    # ─── GENERAL ─────────────────────────────
    APP_NAME: str = Field(..., alias="APP_NAME")
    APP_ENV: str = Field(..., alias="APP_ENV")
    APP_PORT: int = Field(..., alias="APP_PORT")

    # ─── DATABASE ────────────────────────────
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")

    # ─── REDIS ───────────────────────────────
    REDIS_URL: str = Field(..., alias="REDIS_URL")

    # ─── SECURITY ────────────────────────────
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field(..., alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── FRONTEND ────────────────────────────
    FRONTEND_URL: str = Field(..., alias="FRONTEND_URL")

    # ─── CONFIGURATION ───────────────────────
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

    def get_effective_database_url(self) -> str:
        """
        Allow dynamic database switching or formatting in the future if needed.
        """
        return self.DATABASE_URL

# Initialize once for the entire app
settings = Settings()

# Structured, non-blocking confirmation for production logs
logger.info(f"✅ Dealcross settings loaded: {settings.APP_NAME} ({settings.APP_ENV})")
logger.info(f"✅ Redis URL: {settings.REDIS_URL}")