# File: admin_setup.py
import os
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise
from project_config.dealcross_config import settings
from core.security import verify_password
from admin_views.change_password_view import router as change_password_view
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()
print("✅ .env loaded in admin_setup.")

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

admin_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "admin_static")
admin_app.mount("/admin/static", StaticFiles(directory=STATIC_DIR), name="static")

@admin_app.on_event("startup")
async def startup():
    print("🚀 Starting FastAPI Admin initialization...")
    try:
        await Tortoise.init(db_url=settings.database_url, modules={"models": ["models"]})
        print("✅ Tortoise initialized for FastAPI Admin.")
    except Exception as e:
        print(f"❌ Tortoise initialization failed: {e}")

    try:
        await admin_app.configure(
            logo_url="https://dealcross.net/logo192.png",
            favicon_url="https://dealcross.net/favicon.ico",
            admin_path="/admin",
            template_folders=[TEMPLATE_DIR],
            providers=[
                UsernamePasswordProvider(
                    admin_model="models.admin.Admin",
                    verify_password=verify_password,
                    username_field="email",
                )
            ],
            redis=redis_client,
        )
        print("✅ FastAPI Admin configured successfully.")
    except Exception as e:
        print(f"❌ FastAPI Admin configuration failed: {e}")

admin_app.include_router(change_password_view, prefix="/admin")