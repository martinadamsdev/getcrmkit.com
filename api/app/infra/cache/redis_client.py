from redis.asyncio import Redis, from_url

from app.config.settings import get_settings


def create_redis_client() -> Redis:
    settings = get_settings()
    return from_url(
        settings.redis_url,
        decode_responses=True,
    )


redis_client = create_redis_client()
