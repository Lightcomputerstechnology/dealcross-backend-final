import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from datetime import datetime, timedelta

# ──────────────── Load .env explicitly ────────────────
from dotenv import load_dotenv
load_dotenv()
print("✅ .env loaded successfully.")

# ──────────────── Core imports ────────────────
from core.database import init_db, close_db
from core.middleware import RateLimitMiddleware
from core.security import get_password_hash, verify_password
from project_config.dealcross_config import settings

# ──────────────── Admin setup ────────────────
from admin_setup import admin_app

# ──────────────── Redis setup ────────────────
import redis.asyncio as redis

print("✅ ENV REDIS_URL:", os.getenv("REDIS_URL"))
print("✅ settings.redis_url:", settings.redis_url)

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# ──────────────── Routers ────────────────
from routers import user_2fa, contact, payment_webhooks
from routers.user import router as user_router
from routers.wallet import router as wallet_router
from routers.deals import router as deals_router
from routers.kyc import router as kyc_router
from routers.admin_wallet import router as admin_wallet_router
from routers.admin_referrals import router as admin_referrals_router
from routers.admin_kyc import router as admin_kyc_router
from routers.chart import router as chart_router
from routers.chat import router as chat_router
from routers.health import router as health_router
from routers.subscription import router as subscription_router
from app.api.routes import router as api_router

# ──────────────── Utils ────────────────
from utils import otp as otp_utils
from utils import email_otp as email_otp_utils
from utils import send_email

# ──────────────── OAuth2 ────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ──────────────── FastAPI initialization ────────────────
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for the Dealcross platform"
)

# make redis available to routers if needed
app.state.redis = redis_client  # ✅ expose redis client

# ──────────────── Secure One-Time Admin Seeder ────────────────
async def seed_admin_if_missing():
    from tortoise.transactions import in_transaction
    from models import admin as admin_model
    from passlib.hash import bcrypt

    admin_email = "admin@dealcross.com"
    admin_password = "AdminPass123!"

    async with in_transaction():
        existing = await admin_model.Admin.get_or_none(email=admin_email)
        if not existing:
            print(f"✅ Seeding admin user {admin_email}...")
            await admin_model.Admin.create(
                email=admin_email,
                hashed_password=bcrypt.hash(admin_password),
                is_superuser=True,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            print(f"✅ Admin created: {admin_email} / {admin_password}")
        else:
            print(f"✅ Admin user {admin_email} already exists, skipping seeding.")

# ──────────────── Startup and Shutdown ────────────────
@app.on_event("startup")
async def on_startup():
    print("🚀 Starting up... initializing DB.")
    try:
        await init_db()
        await seed_admin_if_missing()  # ✅ AUTO-SEED ADMIN ON FIRST DEPLOY

        # ⚠️ REMOVE THIS CALL AFTER YOU HAVE LOGGED IN TO ADMIN PANEL TO TIGHTEN SECURITY:
        # await seed_admin_if_missing()

        print("✅ DB initialized successfully.")
    except Exception as e:
        print("❌ DB initialization failed:", e)

@app.on_event("shutdown")
async def on_shutdown():
    print("🛑 Shutting down... closing DB.")
    await close_db()
    print("✅ DB closed successfully.")

# ──────────────── Middleware ────────────────
app.add_middleware(RateLimitMiddleware)

# ✅ Tighten CORS to your real frontend + local dev
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
print("✅ FRONTEND_URL:", FRONTEND_URL)

allow_origins = list({
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://dealcross.net",  # keep your prod domain explicit
})

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────── Admin Mount ────────────────
app.mount("/admin", admin_app)

# ──────────────── API Routers ────────────────
app.include_router(user_2fa.router)
app.include_router(contact.router)
app.include_router(user_router, prefix="/user")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(deals_router, prefix="/deals")
app.include_router(kyc_router, prefix="/kyc")
app.include_router(admin_wallet_router, prefix="/admin-wallet")
app.include_router(admin_referrals_router)
app.include_router(admin_kyc_router, prefix="/admin/kyc")
app.include_router(chart_router, prefix="/chart")
app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")
app.include_router(subscription_router, prefix="/subscription")
app.include_router(api_router)
app.include_router(payment_webhooks.router, prefix="/webhooks")

# ──────────────── Root Landing Route ────────────────
@app.get("/")
async def root():
    return {
        "message": "✅ Dealcross backend is live and working.",
        "status": "ok",
        "docs": "/docs",
        "admin": "/admin"
    }

@app.on_event("startup")
async def startup_admin_app():
    print("🚀 Manually initializing FastAPI Admin...")
    await admin_app.router.startup()
    print("✅ FastAPI Admin initialized manually.")
