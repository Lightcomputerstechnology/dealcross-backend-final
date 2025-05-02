from pydantic_settings import BaseSettings  # or 'from pydantic import BaseSettings' for v1

class Settings(BaseSettings):
    # Core Auth Settings
    SECRET_KEY: str
    ALGORITHM: str

    # DB Settings
    DATABASE_URL: str

    # Optional Email Configs (won’t fail validation if not used)
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"  # ✅ This fixes the ValidationError for any unused/extra vars

settings = Settings()