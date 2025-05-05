# admin_setup.py

from fastapi import FastAPI
from fastapi_admin.factory import app as admin_app
from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from tortoise.contrib.fastapi import register_tortoise
from config import settings

# Secure FastAPI admin instance
app = FastAPI(title="Dealcross Admin", docs_url=None, redoc_url=None)

@app.on_event("startup")
async def startup():
    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",  # Custom logo
        template_folders=[],
        providers=[
            UsernamePasswordProvider(
                admin_model="models.user.User",
                login_logo_url="https://dealcross-frontend.onrender.com/logo192.png",
                login_title="Dealcross Admin Login",
                login_description="Welcome back, Admin.",
            )
        ],
        admin_path="/admin",
        admin_secret="supersecretadminkey",  # Optional
        title="Dealcross Admin",
        favicon_url="https://dealcross-frontend.onrender.com/favicon.ico"
    )

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": [
        "models.user",
        "models.kyc",
        "models.wallet",
        "models.wallet_transaction",
        "models.admin_wallet",
        "models.deal",
        "models.fraud",
        "models.audit_log",
        "models.dispute",
        "aerich.models"
    ]},
    generate_schemas=False
)