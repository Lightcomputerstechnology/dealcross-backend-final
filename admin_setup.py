from fastapi import FastAPI
from fastapi_admin.factory import app as admin_app
from fastapi_admin.app import FastAPIAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.requests import Request

from tortoise.contrib.fastapi import register_tortoise
from config import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    await admin_app.configure(
        logo_url="https://dealcross.onrender.com/logo.png",  # You can replace with your logo
        template_folders=[],
        providers=[
            UsernamePasswordProvider(
                admin_model='models.user.User',
                login_logo_url="https://dealcross.onrender.com/logo.png",
            )
        ],
        admin_secret="supersecretadminkey",  # Optional custom key
    )

# Tortoise ORM init
register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["models.user"]},
    generate_schemas=False
)

app.mount("/admin", admin_app)