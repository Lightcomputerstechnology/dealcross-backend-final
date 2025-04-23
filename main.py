# File: main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.database import Base, engine
from core.middleware import RateLimitMiddleware

# our one “master router”
from app.api.routes import include_all_routes

# 1) Create tables (we run Alembic migrations separately)
Base.metadata.create_all(bind=engine)

# 2) Initialize app
app = FastAPI(
    title="Dealcross Backend",
    version="1.0.0",
    description=(
        "FastAPI backend powering the Dealcross platform "
        "with escrow, analytics, fraud detection, admin controls, and more."
    ),
)

# 3) Middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # tighten in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4) Mount every router in one go
app.include_router(include_all_routes())

# 5) Global exception handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "code": exc.status_code, "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "code": 400,
            "message": "Validation error",
            "details": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": True, "code": 500, "message": "Internal server error"},
    )
