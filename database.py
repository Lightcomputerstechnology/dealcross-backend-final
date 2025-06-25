from tortoise import Tortoise
from config import settings  # Load from .env

async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models.__models__"]}
    )
    # await Tortoise.generate_schemas()  # ❌ Skip if using Aerich

async def close_db():
    await Tortoise.close_connections()