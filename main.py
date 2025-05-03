# File: main.py

import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from core.db import init_db, close_db
from core.middleware import RateLimitMiddleware

from app.api.routes import router as api_router
from routers.chart import router as chart_router
from routers.chat import router as chat_router
from routers.health import router as health_router
from routers.subscription import router as subscription_router
from routers.user import router as user_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description=(
        "FastAPI backend for the Dealcross platform including escrow, wallet, "
        "analytics, subscription, and more."
    )
)

# ──────────────────────────────────────────────
# LIFECYCLE EVENTS
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
    allow_origins=["*"],  # TODO: Replace with allowed frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

app.include_router(user_router, prefix="/user")
app.include_router(api_router)
app.include_router(chart_router, prefix="/chart")
app.include_router(chat_router, prefix="/chat")
app.include_router(health_router, prefix="/health")
app.include_router(subscription_router, prefix="/subscription")

# ──────────────────────────────────────────────
# PLAN UPGRADE ENDPOINT (Demo Only)
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

    # TODO: integrate real payment logic
    payment_success = True
    if not payment_success:
        raise HTTPException(status_code=400, detail="Payment failed.")

    return {"message": f"Upgraded to {plan} plan successfully."}
