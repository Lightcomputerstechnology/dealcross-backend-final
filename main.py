from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.db import init_db, close_db  # Corrected path
from core.middleware import RateLimitMiddleware  # Corrected path
from app.api.routes import router as api_router  # Corrected path

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics."
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)
