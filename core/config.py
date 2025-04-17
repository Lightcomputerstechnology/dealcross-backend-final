from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: list[str] = ["*"]  # You can change this to specific domains for production

    class Config:
        env_file = ".env"


settings = Settings()
