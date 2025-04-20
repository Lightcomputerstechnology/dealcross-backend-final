from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin           # Core feature routers
from routers import analytics                                      # Admin metrics
from app.api.routes.admin import fraud                             # NEW: Fraud report router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration — secure origins for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TIP: Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth.router,       prefix="/auth",      tags=["Authentication"])
app.include_router(wallet.router,     prefix="/wallet",    tags=["Wallet"])
app.include_router(deals.router,      prefix="/deals",     tags=["Deals"])
app.include_router(disputes.router,   prefix="/disputes",  tags=["Disputes"])
app.include_router(admin.router,      prefix="/admin",     tags=["Admin Core"])
app.include_router(analytics.router,  prefix="/admin",     tags=["Admin Analytics"])
app.include_router(fraud.router,      prefix="/admin",     tags=["Fraud Reports"])  # NEW: Logs fraud activity
