from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.settings import get_settings


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture
async def db_session(settings) -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    conn = await engine.connect()
    txn = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    yield session
    await txn.rollback()
    await conn.close()
    await engine.dispose()


@pytest.fixture
async def redis(settings) -> AsyncGenerator[Redis]:
    client = Redis.from_url(settings.redis_url, decode_responses=True)
    yield client
    await client.aclose()


@pytest.fixture
async def client(settings) -> AsyncGenerator[AsyncClient]:
    from app.application.shared.unit_of_work import AbstractUnitOfWork
    from app.infra.database.unit_of_work import SqlAlchemyUnitOfWork
    from app.interfaces.api.deps import get_db, get_redis, get_uow
    from app.main import create_app

    test_engine = create_async_engine(settings.database_url, poolclass=NullPool)
    conn = await test_engine.connect()
    txn = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)

    # Create a test Redis client and flush test keys after
    test_redis = Redis.from_url(settings.redis_url, decode_responses=True)

    app = create_app()

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        yield session

    async def override_get_redis() -> Redis:
        return test_redis

    async def override_get_uow() -> AsyncGenerator[AbstractUnitOfWork]:
        uow = SqlAlchemyUnitOfWork.__new__(SqlAlchemyUnitOfWork)
        uow.session = session
        yield uow

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_uow] = override_get_uow

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await txn.rollback()
    await conn.close()
    await test_engine.dispose()
    await test_redis.flushdb()
    await test_redis.aclose()


@pytest.fixture
async def authenticated_client(client: AsyncClient) -> AsyncGenerator[AsyncClient]:
    """Register a user and return a client with auth headers."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "Secure123",
            "name": "Test User",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "Secure123",
        },
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    yield client
