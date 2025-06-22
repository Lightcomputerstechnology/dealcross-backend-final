# admin_setup.py
import os
from fastapi_admin.app import app as admin_app  # ✅ This is the one to expose
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

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
    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",
        template_folders=[TEMPLATE_DIR],
        providers=[
            UsernamePasswordProvider(
                admin_model="models.user.User",
                verify_password=verify_password,
                username_field="username"
            )
        ],
        admin_path="/admin",
        title="Dealcross Admin",
        favicon_url="https://dealcross-frontend.onrender.com/favicon.ico"
    )

# ──────────────────────────────────────────────
# Tortoise ORM
# ──────────────────────────────────────────────

register_tortoise(
    admin_app,
    db_url=settings.DATABASE_URL,
    modules={"models": [
        "models.user",
        "models.wallet",
        "models.wallet_transaction",
        "models.admin_wallet",
        "models.kyc",
        "models.deal",
        "models.dispute",
        "models.fraud",
        "models.audit_log",
        "models.metric",
        "models.chart",
        "models.chat",
        "models.login_attempt",
        "models.platform_earnings",
        "models.referral_reward",
        "models.support",
        "models.share",
        "models.settings",
        "models.pending_approval",
        "models.banner",
        "models.role",
        "models.webhook",
        "models.notification",
        "models.investor_report",
        "models.escrow",
        "aerich.models"
    ]},
    generate_schemas=False
)

# ──────────────────────────────────────────────
# CUSTOM ADMIN ROUTES
# ──────────────────────────────────────────────

admin_app.include_router(change_password_view, prefix="/admin")