from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, wallet, deals, disputes, admin
from core.database import get_db, engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
