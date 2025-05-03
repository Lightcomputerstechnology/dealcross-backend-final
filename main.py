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

from tortoise.contrib.fastapi import register_tortoise

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description=(
        "FastAPI backend for Dealcross platform including escrow, wallet, "
        "analytics, subscription, and more."
    )
)

# ─── Lifecycle Events ─────────────────────────
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# ─── Middleware ───────────────────────────────
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API Routes ───────────────────────────────
app.include_router(user_router)            # /users
app.include_router(api_router)             # grouped API endpoints
app.include_router(chart_router)           # /chart
app.include_router(chat_router)            # /chat
app.include_router(health_router)          # /health
app.include_router(subscription_router)    # /subscription

# ─── Subscription Plan Upgrade ─────────────
@app.post("/users/upgrade-plan")
async def upgrade_plan(
    request: Request,
    plan: str,
    payment_method: str,
    token: str = Depends(oauth2_scheme)
):
    if plan not in ("pro", "business"):
        raise HTTPException(status_code=400, detail="Invalid plan selected.")

    # TODO: integrate real payment gateway here
    payment_success = True
    if not payment_success:
        raise HTTPException(status_code=400, detail="Payment failed.")

    return {"message": f"Upgraded to {plan} plan successfully."}

# ─── Tortoise ORM Setup ──────────────────────
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL", "sqlite://db.sqlite3"),
    modules={"models": ["models.user"]},
    generate_schemas=True,          # auto-create tables in dev
    add_exception_handlers=True     # handle 404 for missing objects
)
