from redis.asyncio import Redis


class TokenBlacklist:
    PREFIX = "token:blacklist:"

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def add(self, jti: str, ttl: int) -> None:
        if ttl > 0:
            await self._redis.setex(f"{self.PREFIX}{jti}", ttl, "1")

    async def is_blacklisted(self, jti: str) -> bool:
        result = await self._redis.get(f"{self.PREFIX}{jti}")
        return result is not None
