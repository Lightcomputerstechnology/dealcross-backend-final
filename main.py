from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin  # Existing routers
from routers import analytics  # NEW: Admin analytics router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware (enable frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router,       prefix="/auth",      tags=["Authentication"])
app.include_router(wallet.router,     prefix="/wallet",    tags=["Wallet"])
app.include_router(deals.router,      prefix="/deals",     tags=["Deals"])
app.include_router(disputes.router,   prefix="/disputes",  tags=["Disputes"])
app.include_router(admin.router,      prefix="/admin",     tags=["Admin"])
app.include_router(analytics.router,  prefix="/admin",     tags=["Admin Analytics"])  # NEW analytics metrics endpoint
