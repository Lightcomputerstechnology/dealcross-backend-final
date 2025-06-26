# File: admin_setup.py

import os
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view

# ───────────────────────────────
# Middleware
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
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

# ───────────────────────────────
# Startup Event
# ───────────────────────────────
@admin_app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models.admin", "models.user", "models.wallet", "models.deal"]},  # ✅ Add all model modules
    )

    await admin_app.configure(
        logo_url="https://dealcross.net/logo192.png",
        favicon_url="https://dealcross.net/favicon.ico",
        template_folders=[TEMPLATE_DIR],
        title="Dealcross Admin",
        admin_path="/admin",
        providers=[
            UsernamePasswordProvider(
                admin_model="models.admin.Admin",  # ✅ This should point to your actual Admin model
                verify_password=verify_password,
                username_field="username"
            )
        ]
    )

# ───────────────────────────────
# Extra Custom Admin Routes
# ───────────────────────────────
admin_app.include_router(change_password_view, prefix="/admin")