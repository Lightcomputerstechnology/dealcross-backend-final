from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # General
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # Database
    database_url: str = Field(..., alias="DATABASE_URL")

    # Security
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Redis
    redis_url: str = Field(..., alias="REDIS_URL")

    # Email
    smtp_server: str = Field(..., alias="EMAIL_HOST")
    smtp_port: int = Field(..., alias="EMAIL_PORT")
    smtp_username: str = Field(..., alias="EMAIL_USER")
    smtp_password: str = Field(..., alias="EMAIL_PASSWORD")
    smtp_from: str = Field(..., alias="EMAIL_FROM_NAME")

    # Frontend
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

settings = Settings()