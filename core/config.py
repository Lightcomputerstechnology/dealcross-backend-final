from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    redis_url: str = Field(..., alias="REDIS_URL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

settings = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": settings.database_url,
    },
    "apps": {
        "models": {
            "models": [
                "models",         # <- will pick up all models with __models__ inside
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}