# config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env using absolute path
env_path = Path(__file__).parent.parent / '.env'
print(f"Loading .env from: {env_path.resolve()}")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Core Auth Settings
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")

    # Database
    database_url: str | None = Field(None, env="DATABASE_URL")
    db_host: str = Field("", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_user: str = Field("", env="DB_USER")
    db_password: str = Field("", env="DB_PASSWORD")
    db_name: str = Field("", env="DB_NAME")

    # Redis
    redis_url: str = Field("", env="REDIS_URL")

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def effective_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if self.db_user and self.db_password and self.db_host and self.db_name:
            return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        raise ValueError("DATABASE_URL is not set and DB connection parts are incomplete.")

settings = Settings()

# Debug dump for Render verification
print("[DEBUG] settings.database_url:", settings.database_url)
print("[DEBUG] settings.effective_database_url:", settings.effective_database_url)
print("[DEBUG] settings.secret_key:", settings.secret_key)
print("[DEBUG] settings.redis_url:", settings.redis_url)