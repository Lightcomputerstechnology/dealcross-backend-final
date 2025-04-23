# File: app/api/routes/__init__.py
# File: main.py

from fastapi import FastAPI
from app.api.routes import include_all_routes

app = FastAPI()

# Include all routes
app.include_router(include_all_routes())
