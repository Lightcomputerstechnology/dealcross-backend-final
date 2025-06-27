# File: admin_setup.py

import os
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view

# Optional: Redis session backend if you want admin login session scalability
import redis.asyncio as redis

# ───────────────────────────────
# Redis client for scalable admin sessions
# ───────────────────────────────
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# ───────────────────────────────
# CORS Middleware
# ───────────────────────────────
admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────
# Template Folder Setup
# ───────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ───────────────────────────────
# Startup Event
# ───────────────────────────────
@admin_app.on_event("startup")
async def startup():
    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models"]},  # Load all models via models/__init__.py
    )

    # Ensure schemas are generated (only for development)
    if settings.DEBUG:
        await Tortoise.generate_schemas()

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
                username_field="email",  # Uses email as username field
            )
        ],
        redis=redis_client  # Allows scalable admin sessions
    )

# ───────────────────────────────
# Custom Admin Routes
# ───────────────────────────────
admin_app.include_router(change_password_view, prefix="/admin")