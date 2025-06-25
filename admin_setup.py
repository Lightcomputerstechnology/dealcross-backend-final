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
        modules={"models": ["models"]},  # ✅ This must match your models/__init__.py setup
    )

    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",
        favicon_url="https://dealcross-frontend.onrender.com/favicon.ico",
        title="Dealcross Admin",
        admin_path="/admin",
        template_folders=[TEMPLATE_DIR],
        providers=[
            UsernamePasswordProvider(
                admin_model="models.User",  # ✅ FIXED: must be "models.ModelName"
                verify_password=verify_password,
                username_field="username"
            )
        ]
    )

# ───────────────────────────────
# Extra Custom Admin Routes
# ───────────────────────────────
admin_app.include_router(change_password_view, prefix="/admin")