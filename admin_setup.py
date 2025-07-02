import os
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from project_config.dealcross_config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view
import redis.asyncio as redis

# ──────────────── Load .env explicitly ────────────────
from dotenv import load_dotenv
load_dotenv()
print("✅ .env loaded successfully in admin_setup.")

# Debug prints to verify REDIS_URL loading
print("✅ ENV REDIS_URL:", os.getenv("REDIS_URL"))
print("✅ settings.redis_url:", settings.redis_url)

# Redis client for session backend
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# CORS Middleware for Admin
admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template folder setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Startup event for Admin
@admin_app.on_event("startup")
async def startup():
    print("🚀 Starting up FastAPI Admin... initializing Tortoise.")
    try:
        await Tortoise.init(
            db_url=settings.database_url,
            modules={"models": ["models"]},
        )
        print("✅ Tortoise initialized successfully in admin_setup.")
    except Exception as e:
        print("❌ Tortoise initialization failed in admin_setup:", e)

    try:
        await admin_app.configure(
            logo_url="https://dealcross.net/logo192.png",
            favicon_url="https://dealcross.net/favicon.ico",
            title="Dealcross Admin",
            admin_path="/admin",
            template_folders=[TEMPLATE_DIR],
            providers=[
                UsernamePasswordProvider(
                    admin_model="models.admin.Admin",
                    verify_password=verify_password,
                    username_field="email",
                )
            ],
            redis=redis_client
        )
        print("✅ FastAPI Admin configured successfully.")
    except Exception as e:
        print("❌ FastAPI Admin configuration failed:", e)

# Ensure change_password_view is mounted
admin_app.include_router(change_password_view, prefix="/admin")
