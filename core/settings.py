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
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # ─── DATABASE ────────────────────────────
    database_url: str = Field(..., alias="DATABASE_URL")

    # ─── REDIS ───────────────────────────────
    redis_url: str = Field(..., alias="REDIS_URL")

    # ─── SECURITY ────────────────────────────
    jwt_secret: str = Field(..., alias="JWT_SECRET")    # ✅ updated to match your .env
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── FRONTEND ────────────────────────────
    frontend_url: str = Field(..., alias="FRONTEND_URL")

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
        return self.database_url

# Initialize once for the entire app
settings = Settings()

# Structured, non-blocking confirmation for production logs
logger.info(f"✅ Dealcross settings loaded: {settings.app_name} ({settings.app_env})")
logger.info(f"✅ Redis URL: {settings.redis_url}")