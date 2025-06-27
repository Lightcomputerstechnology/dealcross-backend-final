# File: main.py

import os

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from starlette.responses import JSONResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# Core imports
from core.database import init_db, close_db
from core.middleware import RateLimitMiddleware
from core.security import get_password_hash, verify_password
from core.config import settings

# ─────────────────────────────────────────────
# Admin panel
from admin_setup import admin_app
from admin_views.change_password_view import router as change_password_view

# ─────────────────────────────────────────────
# Redis for session & 2FA sessions
import redis.asyncio as redis

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# ─────────────────────────────────────────────
# Routers
from routers import contact, payment_webhooks
from routers.user import router as user_router
from routers.wallet import router as wallet_router
from routers.deals import router as deals_router
from routers.kyc import router as kyc_router
from routers.admin_wallet import router as admin_wallet_router
from routers.admin_referral import router as admin_referral_router
from routers.admin_kyc import router as admin_kyc_router
from routers.chart import router as chart_router
from routers.chat import router as chat_router
from routers.health import router as health_router
from routers.subscription import router as subscription_router
from app.api.routes import router as api_router

# ─────────────────────────────────────────────
# Utils for OTP and TOTP
from utils import otp as otp_utils
from utils import email_otp as email_otp_utils
from utils import send_email

# ─────────────────────────────────────────────
# Auth schema and user model
from schemas.user_schema import UserCreate, UserOut
from models.user import User

# ─────────────────────────────────────────────
# OAuth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─────────────────────────────────────────────
# FastAPI App Initialization
# ─────────────────────────────────────────────
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for the Dealcross platform"
)

# ─────────────────────────────────────────────
# Startup / Shutdown
# ─────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Mount admin panel
# ─────────────────────────────────────────────
app.mount("/admin", admin_app)
app.include_router(change_password_view, prefix="/admin")

# ─────────────────────────────────────────────
# API Routers
# ─────────────────────────────────────────────
app.include_router(contact.router)
app.include_router(user_router, prefix="/user")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(deals_router, prefix="/deals")
app.include_router(kyc_router, prefix="/kyc")
app.include_router(admin_wallet_router, prefix="/admin-wallet")
app.include_router(admin_referral_router, prefix="/admin-referral")
app.include_router(admin_kyc_router, prefix="/admin/kyc")
app.include_router(chart_router, prefix="/chart")
app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")
app.include_router(subscription_router, prefix="/subscription")
app.include_router(api_router)
app.include_router(payment_webhooks.router, prefix="/webhooks")

# ─────────────────────────────────────────────
# Sample extra route for upgrade plan
# ─────────────────────────────────────────────
@app.post("/users/upgrade-plan")
async def upgrade_plan(
    request: Request,
    plan: str,
    payment_method: str,
    token: str = Depends(oauth2_scheme)
):
    if plan not in ("pro", "business"):
        raise HTTPException(status_code=400, detail="Invalid plan selected.")
    return {"message": f"Upgraded to {plan} plan successfully."}