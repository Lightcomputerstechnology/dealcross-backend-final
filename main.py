from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import HTTPException as FastAPIHTTPException

from core.database import SessionLocal, get_db
from core.middleware import RateLimitMiddleware
from models.admin_wallet import AdminWallet

import models  # ✅ Import ALL models

from app.api.routes import router as api_router

app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="FastAPI backend for Dealcross platform including escrow, wallet, and analytics.",
)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if not db.query(AdminWallet).first():
        db.add(AdminWallet(balance=0.00))
        db.commit()
    db.close()

# Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # lock down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)

import models  # ✅ Load all models
from core.database import engine, Base

# ✅ Ensure tables are created once
Base.metadata.create_all(bind=engine)
