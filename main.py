from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Dealcross API",
    description="Backend API for Dealcross platform",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(disputes.router, prefix="/disputes", tags=["Disputes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Dealcross API"}

# Uvicorn entrypoint for Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=False)
