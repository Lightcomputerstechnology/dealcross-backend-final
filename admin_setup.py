import os
from fastapi_admin.app import app as admin_app  # ✅ This is the one to expose
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view

# ──────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────

admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# STARTUP CONFIG
# ──────────────────────────────────────────────

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

@admin_app.on_event("startup")
async def startup():
    # ✅ Initialize Tortoise manually before calling configure
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models"]},  # This points to your __init__.py with all models imported
    )

    # Optional: Ensure schemas are synced (or skip if using Aerich)
    # await Tortoise.generate_schemas(safe=True)

    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",
        template_folders=[TEMPLATE_DIR],
        providers=[
            UsernamePasswordProvider(
                admin_model="models.User",  # This string is now correctly resolved
                verify_password=verify_password,
                username_field="username"
            )
        ],
        admin_path="/admin",
        title="Dealcross Admin",
        favicon_url="https://dealcross-frontend.onrender.com/favicon.ico"
    )

# ──────────────────────────────────────────────
# CUSTOM ADMIN ROUTES
# ──────────────────────────────────────────────

admin_app.include_router(change_password_view, prefix="/admin")
