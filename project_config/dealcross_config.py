from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
import logging

logger = logging.getLogger("dealcross.settings")
logging.basicConfig(level=logging.INFO)


class DealcrossSettings(BaseSettings):
    """
    Single source of truth for all environment configuration.
    Safe logging (no secret values).
    """

    # ─── GENERAL ─────────────────────────────
    app_name: str = Field(..., alias="APP_NAME")
    app_env: str = Field(..., alias="APP_ENV")
    app_port: int = Field(..., alias="APP_PORT")

    # ─── DATABASE ────────────────────────────
    database_url: str = Field(..., alias="DATABASE_URL")

    # ─── REDIS ───────────────────────────────
    redis_url: str = Field(..., alias="REDIS_URL")

    # ─── SECURITY / JWT (legacy local use) ───
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ─── FRONTEND ────────────────────────────
    frontend_url: str = Field(..., alias="FRONTEND_URL")

    # ─── SUPABASE AUTH ───────────────────────
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_jwks_url: str = Field(..., alias="SUPABASE_JWKS_URL")
    supabase_service_role: str = Field(..., alias="SUPABASE_SERVICE_ROLE")
    # Optional for backend (frontend must use anon). Keep for rare server calls if needed.
    supabase_anon_key: str | None = Field(None, alias="SUPABASE_ANON_KEY")

    # ─── PAYMENT GATEWAYS ────────────────────
    paystack_secret: str = Field(..., alias="PAYSTACK_SECRET")
    flw_secret: str = Field(..., alias="FLW_SECRET")
    nowpay_api_key: str = Field(..., alias="NOWPAY_API_KEY")

    # ─── EMAIL SENDER ────────────────────────
    email_host: str = Field(..., alias="EMAIL_HOST")
    email_port: int = Field(587, alias="EMAIL_PORT")
    email_user: str = Field(..., alias="EMAIL_USER")
    email_password: str = Field(..., alias="EMAIL_PASSWORD")
    email_from_name: str = Field("Dealcross", alias="EMAIL_FROM_NAME")
    otp_issuer_name: str = Field("Dealcross", alias="OTP_ISSUER_NAME")

    # ─── RATE LIMIT ──────────────────────────
    rate_limit_max_requests: int = Field(100, alias="RATE_LIMIT_MAX_REQUESTS")
    rate_limit_time_window: int = Field(60, alias="RATE_LIMIT_TIME_WINDOW")

    # ─── CALLBACK / WEBHOOKS ─────────────────
    paystack_callback: str = Field(..., alias="PAYSTACK_CALLBACK")
    flutterwave_callback: str = Field(..., alias="FLUTTERWAVE_CALLBACK")
    nowpay_callback: str = Field(..., alias="NOWPAY_CALLBACK")

    # ─── Pydantic Settings Config ────────────
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }

    @model_validator(mode="after")
    def _critical_checks(self):
        # Minimal hard guards
        critical = [
            "database_url",
            "redis_url",
            "jwt_secret",
            "supabase_url",
            "supabase_jwks_url",
            "supabase_service_role",
        ]
        for f in critical:
            if not getattr(self, f, None):
                raise ValueError(f"{f} is required in environment configuration")
        return self

    def get_effective_database_url(self) -> str:
        """
        Tortoise expects 'postgres://'. Normalize if 'postgresql://' is provided.
        """
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgres://", 1)
        return url


# Instantiate once for app-wide usage
settings = DealcrossSettings()

# Safe, non-secret logs
logger.info("✅ Settings loaded")
logger.info(f"• App: {settings.app_name} [{settings.app_env}]")
logger.info("• DATABASE_URL loaded")
logger.info("• REDIS_URL loaded")
logger.info("• SUPABASE_URL loaded")
logger.info("• SUPABASE_JWKS_URL loaded")
logger.info("• SUPABASE_SERVICE_ROLE loaded")
logger.info("• Email/Payment configuration loaded")
