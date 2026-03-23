import pytest
from redis.asyncio import Redis


@pytest.mark.asyncio
async def test_redis_ping(redis: Redis):
    assert await redis.ping() is True


@pytest.mark.asyncio
async def test_redis_set_get(redis: Redis):
    await redis.set("test_key", "test_value")
    value = await redis.get("test_key")
    assert value == "test_value"
    await redis.delete("test_key")
