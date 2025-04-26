File: core/database.py

import os from sqlalchemy import create_engine from sqlalchemy.orm import sessionmaker, declarative_base from contextlib import contextmanager

▶ 1. Read DATABASE_URL from env

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

▶ 2. Create engine & session factory

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True) SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

▶ 3. Declare your base

Base = declarative_base()

▶ 4. Auto-create all tables & indexes at startup

checkfirst=True skips any that already exist

def init_db(): """ Auto-create tables for all models bound to Base metadata. Call this on application startup. """ Base.metadata.create_all(bind=engine, checkfirst=True)

▶ 5. DB session dependency

@contextmanager

def get_db(): db = SessionLocal() try: yield db finally: db.close()

File: main.py (excerpt showing startup)

from fastapi import FastAPI, Request from fastapi.middleware.cors import CORSMiddleware from fastapi.responses import JSONResponse from fastapi.exceptions import RequestValidationError from starlette.exceptions import HTTPException as StarletteHTTPException from fastapi import HTTPException as FastAPIHTTPException

from core.database import SessionLocal, init_db from core.middleware import RateLimitMiddleware from models.admin_wallet import AdminWallet from app.api.routes import router as api_router

app = FastAPI( title="Dealcross Backend", version="1.0.0", )

===== Application Startup =====

@app.on_event("startup") def startup_event(): # 1) Ensure all tables exist init_db() # 2) Seed admin wallet db = SessionLocal() if not db.query(AdminWallet).first(): db.add(AdminWallet(balance=0.00)) db.commit() db.close()

===== Middleware & Routes =====

app.add_middleware(RateLimitMiddleware) app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], ) app.include_router(api_router)

(Exception handlers follow)

