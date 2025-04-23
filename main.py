# File: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.database import Base, engine
from core.middleware import RateLimitMiddleware

# ← here is our ONE “master” router
from app.api.routes import router as api_router

# 1) Create all tables
Base.metadata.create_all(bind=engine)

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

# 4) Include every route from app/api/routes
app.include_router(api_router)

# 5) Exception handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(req, exc):
    return JSONResponse(status_code=exc.status_code,
                        content={"error": True, "code": exc.status_code, "message": exc.detail})

@app.exception_handler(RequestValidationError)
async def val_exc_handler(req, exc):
    return JSONResponse(status_code=400,
                        content={"error": True, "code": 400,
                                 "message": "Validation error",
                                 "details": exc.errors()})

@app.exception_handler(Exception)
async def uncaught_exc_handler(req, exc):
    return JSONResponse(status_code=500,
                        content={"error": True, "code": 500,
                                 "message": "Internal server error"})
