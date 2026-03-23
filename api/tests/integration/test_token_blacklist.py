from redis.asyncio import Redis

from app.infra.auth.token_blacklist import TokenBlacklist


class TestTokenBlacklist:
    async def test_add_and_check(self, redis: Redis):
        blacklist = TokenBlacklist(redis)
        await blacklist.add("test-jti-1", ttl=60)
        assert await blacklist.is_blacklisted("test-jti-1") is True

    async def test_not_blacklisted(self, redis: Redis):
        blacklist = TokenBlacklist(redis)
        assert await blacklist.is_blacklisted("unknown-jti") is False

    async def test_zero_ttl_not_stored(self, redis: Redis):
        blacklist = TokenBlacklist(redis)
        await blacklist.add("zero-ttl", ttl=0)
        assert await blacklist.is_blacklisted("zero-ttl") is False
