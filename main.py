# File: main.py

from fastapi import FastAPI
from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin

app = FastAPI(
    title="Dealcross API",
    description="Secure escrow and financial services backend for the Dealcross platform",
    version="1.0.0"
)

# Create database tables at startup
Base.metadata.create_all(bind=engine)

# Register application routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Welcome to the Dealcross API!"}
