from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from core.db import init_db, close_db
from core.middleware import RateLimitMiddleware
from app.api.routes import router as api_router
from routers import chart  # ✅ Chart router for admin charts
from routers import chat  # ✅ Chat router for user/admin chat support
from routers import health  # ✅ Health router for server status
from routers import subscription  # ✅ Subscription plan router for upgrades

# Initialize OAuth2PasswordBearer for authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize FastAPI app
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, analytics, subscription, and more."
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
app.include_router(api_router)       # All grouped API endpoints
app.include_router(chart.router)     # ✅ Chart analytics endpoint
app.include_router(chat.router)      # ✅ Chat system endpoint
app.include_router(health.router)    # ✅ Health monitoring endpoint
app.include_router(subscription.router)  # ✅ Subscription API for handling plan upgrades

# ─── Subscription Plan Upgrade Endpoint ─────────────────────
@app.post("/users/upgrade-plan")
async def upgrade_plan(request: Request, plan: str, payment_method: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint to upgrade the user's subscription plan.
    """
    try:
        # Mocked for now: Process the upgrade logic (validation and payment gateway call)
        if plan not in ['pro', 'business']:
            raise HTTPException(status_code=400, detail="Invalid plan selected.")
        
        # Here we would typically process payment through an external API like Stripe or Paystack.
        # Let's mock a success/failure:
        payment_success = True  # Simulating payment success
        
        if not payment_success:
            raise HTTPException(status_code=400, detail="Payment failed.")
        
        # If payment is successful, update user's subscription in the DB
        # Update user in DB (this is a mock, actual logic should be implemented with DB updates)
        user = {"plan": plan, "payment_method": payment_method}
        return {"message": f"Your account has been upgraded to the {plan} plan successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")