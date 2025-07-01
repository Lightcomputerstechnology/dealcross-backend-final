import asyncio
from tortoise import Tortoise
from core.config import TORTOISE_ORM  # adjust if needed

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)  # forcibly creates tables without constraint issues
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())