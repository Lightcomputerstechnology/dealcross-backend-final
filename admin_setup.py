from fastapi import FastAPI
from fastapi_admin.factory import app as admin_app
from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.requests import Request

from tortoise.contrib.fastapi import register_tortoise
from config import settings

app = FastAPI(title="Dealcross Admin", docs_url=None, redoc_url=None)

@app.on_event("startup")
async def startup():
    await admin_app.configure(
        logo_url="https://dealcross-frontend.onrender.com/logo192.png",  # Custom logo
        template_folders=[],
        providers=[
            UsernamePasswordProvider(
                admin_model='models.user.User',
                login_logo_url="https://dealcross-frontend.onrender.com/logo192.png",
                login_title="Dealcross Admin Login",
                login_description="Welcome back, Admin. Please sign in to manage the platform.",
            )
        ],
        admin_path="/admin",
        admin_secret="supersecretadminkey",  # Optional
        title="Dealcross Admin Dashboard",
        favicon_url="https://dealcross-frontend.onrender.com/favicon.ico",
    )

# Initialize DB
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": [
        "models.user",
        "models.kyc",
        "models.wallet",
        "models.admin_wallet",
        "models.deal",
        "models.dispute",
        "models.fraud",
        "models.audit_log",
        "aerich.models"
    ]},
    generate_schemas=False
)

# Mount admin panel
app.mount("/admin", admin_app)