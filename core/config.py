from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str

    # Email / SMTP Settings
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from: str

    class Config:
        env_file = ".env"

settings = Settings()