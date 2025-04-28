# core/database.py
from tortoise import Tortoise
from config import settings  # Use your existing Pydantic settings

# DATABASE URL for Tortoise ORM (from environment variable)
DATABASE_URL = settings.DATABASE_URL  # This is already stored in the settings

# Initialize the database (Tortoise ORM)
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,  # Use the DATABASE_URL for connection
        modules={"models": ["models"]}  # This tells Tortoise where to find your models
    )
    await Tortoise.generate_schemas()  # Optionally auto-create tables (skip if using Aerich)

# Close DB connection
async def close_db():
    await Tortoise.close_connections()