from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(..., alias="APP_NAME")
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")

    # You can define more as needed...

    class Config:
        env_file = None  # ⛔ Disable local .env on Render
        extra = "ignore"  # ✅ Allow undeclared variables

settings = Settings()