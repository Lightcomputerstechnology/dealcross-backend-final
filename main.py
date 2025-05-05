# File: main.py

import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from core.db import init_db, close_db
from core.middleware import RateLimitMiddleware
from admin_setup import app as admin_app  # Admin panel app

# Routers
from routers import contact  # ✅ import it
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

# Admin password change view
from admin_views.change_password_view import router as change_password_view

# Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ──────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for the Dealcross platform including escrow, wallet, analytics, subscription, and more."
)

# ──────────────────────────────────────────────
# LIFECYCLE
# ──────────────────────────────────────────────

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

# ──────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────

app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

# Admin Panel
app.mount("/admin", admin_app)

# Admin Custom Routes (like password change)
app.include_router(change_password_view, prefix="/admin")

# User Routes
app.include_router(contact.router)  
app.include_router(user_router, prefix="/user")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(deals_router, prefix="/deals")
app.include_router(kyc_router, prefix="/kyc")

# Admin Routes
app.include_router(admin_wallet_router, prefix="/admin-wallet")
app.include_router(admin_referral_router, prefix="/admin-referral")
app.include_router(admin_kyc_router, prefix="/admin/kyc")

# Other Feature Routes
app.include_router(api_router)
app.include_router(chart_router, prefix="/chart")
app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")
app.include_router(subscription_router, prefix="/subscription")

# ──────────────────────────────────────────────
# DEMO: Plan Upgrade Route
# ──────────────────────────────────────────────

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