from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.config.settings import get_settings


@pytest.fixture
async def authenticated_client_with_session(settings) -> AsyncGenerator[tuple[AsyncClient, AsyncSession]]:
    """Like authenticated_client, but also exposes the DB session for direct model insertion."""
    from app.application.shared.task_queue import AbstractTaskQueue
    from app.application.shared.unit_of_work import AbstractUnitOfWork
    from app.infra.database.unit_of_work import SqlAlchemyUnitOfWork
    from app.interfaces.api.deps import get_db, get_redis, get_task_queue, get_uow
    from app.main import create_app

    _settings = get_settings()
    test_engine = create_async_engine(_settings.database_url, poolclass=NullPool)
    conn = await test_engine.connect()
    txn = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)

    test_redis = Redis.from_url(_settings.redis_url, decode_responses=True)
    app = create_app()

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        yield session

    async def override_get_redis() -> Redis:
        return test_redis

    async def override_get_uow() -> AsyncGenerator[AbstractUnitOfWork]:
        uow = SqlAlchemyUnitOfWork.__new__(SqlAlchemyUnitOfWork)
        uow.session = session
        yield uow

    mock_task_queue = AsyncMock(spec=AbstractTaskQueue)

    def override_get_task_queue() -> AbstractTaskQueue:
        return mock_task_queue

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_uow] = override_get_uow
    app.dependency_overrides[get_task_queue] = override_get_task_queue

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register and login
        await ac.post(
            "/api/v1/auth/register",
            json={
                "email": "test-session@example.com",
                "password": "Secure123",
                "name": "Test User",
            },
        )
        response = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": "test-session@example.com",
                "password": "Secure123",
            },
        )
        token = response.json()["access_token"]
        ac.headers["Authorization"] = f"Bearer {token}"
        yield ac, session

    await txn.rollback()
    await conn.close()
    await test_engine.dispose()
    await test_redis.flushdb()
    await test_redis.aclose()
