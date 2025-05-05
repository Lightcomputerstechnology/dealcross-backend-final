# File: admin_setup.py

from fastapi import FastAPI
from fastapi_admin.factory import app as admin_app
from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from tortoise.contrib.fastapi import register_tortoise
from config import settings
from core.security import verify_password  # Ensure this is implemented

import os

app = FastAPI(title="Dealcross Admin", docs_url=None, redoc_url=None)

@app.on_event("startup")
async def startup():
    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",
        template_folders=[os.path.join(os.path.dirname(__file__), "templates")],  # <<=== add this
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