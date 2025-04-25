from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.database import Base, engine, SessionLocal
from core.middleware import RateLimitMiddleware

# Routers
from app.api.routes import router as api_router

# Models
from models.admin_wallet import AdminWallet

# 1) Create all tables
# ✅ Ensure Admin Wallet exists
def create_admin_wallet():
    db = SessionLocal()
    wallet = db.query(AdminWallet).first()
    if not wallet:
        wallet = AdminWallet(balance=0.00)
        db.add(wallet)
        db.commit()
    db.close()

create_admin_wallet()

# 2) Init FastAPI
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description="… your description …",
)

# 3) Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock this down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4) Include every route
app.include_router(api_router)

# 5) Exception handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import HTTPException as FastAPIHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(req, exc):
    return JSONResponse(status_code=exc.status_code,
                        content=exc.detail if isinstance(exc.detail, dict) else {
                            "error": True,
                            "message": exc.detail,
                            "code": exc.status_code
                        })

@app.exception_handler(FastAPIHTTPException)
async def fastapi_http_exc_handler(req, exc):
    return JSONResponse(status_code=exc.status_code,
                        content=exc.detail if isinstance(exc.detail, dict) else {
                            "error": True,
                            "message": exc.detail,
                            "code": exc.status_code
                        })

@app.exception_handler(RequestValidationError)
async def val_exc_handler(req, exc):
    return JSONResponse(status_code=422,
                        content={
                            "error": True,
                            "message": "Validation error",
                            "details": exc.errors()
                        })

@app.exception_handler(Exception)
async def uncaught_exc_handler(req, exc):
    return JSONResponse(status_code=500,
                        content={
                            "error": True,
                            "message": "Internal server error"
                        })
