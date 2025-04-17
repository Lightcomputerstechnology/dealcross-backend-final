from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from routers import auth, wallet, deals, disputes, admin   # keep any routers you have

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/auth",    tags=["Authentication"])
app.include_router(wallet.router,  prefix="/wallet",  tags=["Wallet"])
app.include_router(deals.router,   prefix="/deals",   tags=["Deals"])
app.include_router(disputes.router,prefix="/disputes",tags=["Disputes"])
app.include_router(admin.router,   prefix="/admin",   tags=["Admin"])
