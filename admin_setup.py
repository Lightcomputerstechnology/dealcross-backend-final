import os
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from project_config.dealcross_config import settings  # ✅ clean import
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view
import redis.asyncio as redis

# Debug prints to verify REDIS_URL loading
print("RENDER ENV REDIS_URL:", os.getenv("REDIS_URL"))
print("settings.redis_url:", settings.redis_url)

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

# Template & Static folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Startup event for Admin
@admin_app.on_event("startup")
async def startup():
    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models"]},
    )

    # ⚠️ Remove automatic schema generation to avoid cyclic FK errors
    # if settings.app_env != "production":
    #     await Tortoise.generate_schemas()

    # Configure FastAPI Admin
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

# ✅ Corrected the split line
admin_app.include_router(change_password_view, prefix="/admin")