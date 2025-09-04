# File: app/core/config.py
from pydantic import BaseModel
import os

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "Dealcross")
    APP_ENV: str = os.getenv("APP_ENV", "production")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_JWKS_URL: str = os.getenv("SUPABASE_JWKS_URL", "")
    # Only for server-side service calls (never expose to clients)
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Optional legacy JWT (if you still mint your own)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

settings = Settings()
