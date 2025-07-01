import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from tortoise import Tortoise
from core.config import TORTOISE_ORM  # now it will work

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())