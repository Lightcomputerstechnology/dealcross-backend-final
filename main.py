from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, wallet, deals, disputes, admin
from database import Base, engine
from core.config import settings

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dealcross API",
    description="Backend for the Dealcross platform.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
