from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.interfaces.api.deps import get_engine, get_redis

router = APIRouter(tags=["system"])


@router.get("/health")
async def health_check(
    engine: AsyncEngine = Depends(get_engine),
    redis: Redis = Depends(get_redis),
) -> dict[str, str]:
    db_status = "connected"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    redis_status = "connected"
    try:
        await redis.ping()
    except Exception:
        redis_status = "disconnected"

    return {
        "status": "ok" if db_status == "connected" and redis_status == "connected" else "degraded",
        "db": db_status,
        "redis": redis_status,
    }
