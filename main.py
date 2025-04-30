# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import init_db, close_db
from core.middleware import RateLimitMiddleware
from app.api.routes import router as api_router
from routers import chart  # ✅ Chart router for admin charts

# Initialize FastAPI app
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics."
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