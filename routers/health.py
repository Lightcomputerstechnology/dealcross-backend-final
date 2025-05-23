# File: routers/health.py

from fastapi import APIRouter
from tortoise.transactions import in_transaction
import time

router = APIRouter()

# Track server start time
start_time = time.time()

@router.get("/health")
async def get_server_health():
    # Check database connection using Tortoise ORM
    try:
        async with in_transaction() as conn:
            await conn.execute_query("SELECT 1")
        db_status = True
    except Exception:
        db_status = False

    # Calculate uptime
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    uptime = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

    return {
        "api_status": True,
        "db_status": db_status,
        "uptime": uptime,
    }
