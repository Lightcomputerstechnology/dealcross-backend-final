import os
from dotenv import load_dotenv
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise
import redis.asyncio as redis

from project_config.dealcross_config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view

# Load .env (for local/dev parity)
load_dotenv()
print("✅ .env loaded in admin_setup.")

# Redis client for admin sessions/rate limit
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# CORS (admin UI)
admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten to your admin origin if you prefer
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "admin_static")

# Mount static files for admin
admin_app.mount("/admin/static", StaticFiles(directory=STATIC_DIR), name="static")

@admin_app.on_event("startup")
async def startup():
    print("🚀 Starting FastAPI Admin initialization...")
    try:
        # Use the effective DB URL (converts postgresql:// → postgres:// if needed)
        await Tortoise.init(
            db_url=settings.get_effective_database_url(),
            modules={"models": [
                # Explicitly include model modules so admin can locate Admin model
                "models.admin",
                "models.user",
                "models.wallet",
                "models.wallet_transaction",
                "models.fee_transaction",
                "models.deal",
                "models.dispute",
                "models.kyc",
                "models.chat",
                "models.admin_wallet",
                "models.admin_wallet_log",
                "models.platform_earnings",
                "models.referral_reward",
                "models.auditlog",
                "models.chart",
            ]},
        )
        print("✅ Tortoise initialized for FastAPI Admin.")
    except Exception as e:
        print(f"❌ Tortoise initialization failed: {e}")

    try:
        # NOTE: Do NOT pass 'title' here; this version doesn't support it.
        await admin_app.configure(
            logo_url="https://dealcross.net/logo192.png",
            favicon_url="https://dealcross.net/favicon.ico",
            admin_path="/admin",
            template_folders=[TEMPLATE_DIR],
            providers=[
                UsernamePasswordProvider(
                    admin_model="models.admin.Admin",
                    verify_password=verify_password,
                    username_field="email",
                )
            ],
            redis=redis_client,
        )
        print("✅ FastAPI Admin configured successfully.")
    except Exception as e:
        print(f"❌ FastAPI Admin configuration failed: {e}")

# Extra admin routes (e.g., change password)
admin_app.include_router(change_password_view, prefix="/admin")