from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.database import Base, engine, SessionLocal
from core.middleware import RateLimitMiddleware

# Routers
from app.api.routes import router as api_router

# Models
from models.admin_wallet import AdminWallet

def create_admin_wallet():
    db = SessionLocal()
    if not db.query(AdminWallet).first():
        db.add(AdminWallet(balance=0.00))
        db.commit()
    db.close()

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="… your description …",
)

# Run wallet-seeding at startup
@app.on_event("startup")
def on_startup():
    create_admin_wallet()

# Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock this down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router)

# Exception handlers...
# (your existing handlers go here)