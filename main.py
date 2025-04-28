from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.db import init_db, close_db  # Corrected path
from src.core.middleware import RateLimitMiddleware  # Corrected path
from src.app.api.routes import router as api_router  # Corrected path

# Initialize FastAPI app
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics."
)

# Startup and shutdown events for Tortoise ORM
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# Middleware: Rate limiting and CORS
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)
