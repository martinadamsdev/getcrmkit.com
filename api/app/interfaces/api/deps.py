import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.shared.task_queue import AbstractTaskQueue
from app.application.shared.unit_of_work import AbstractUnitOfWork
from app.config.settings import Settings, get_settings
from app.domain.auth.entities import User
from app.domain.auth.services import AuthConfig, AuthService
from app.domain.auth.value_objects import Token
from app.infra.auth.token_blacklist import TokenBlacklist
from app.infra.cache.redis_client import redis_client
from app.infra.database.connection import async_session_factory, engine
from app.infra.database.repositories.user_repository import UserRepository
from app.infra.database.unit_of_work import SqlAlchemyUnitOfWork
from app.infra.queue import task_queue

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


async def get_uow() -> AsyncGenerator[AbstractUnitOfWork]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield uow


def get_engine() -> AsyncEngine:
    return engine


def get_redis() -> Redis:
    return redis_client


def get_task_queue() -> AbstractTaskQueue:
    return task_queue


def get_token_blacklist(redis: Redis = Depends(get_redis)) -> TokenBlacklist:
    return TokenBlacklist(redis)


def get_auth_config(settings: Settings = Depends(get_settings)) -> AuthConfig:
    return AuthConfig(
        jwt_secret_key=settings.jwt_secret_key,
        jwt_algorithm=settings.jwt_algorithm,
        access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
        refresh_token_expire_days=settings.jwt_refresh_token_expire_days,
        refresh_token_short_expire_hours=settings.jwt_refresh_token_short_expire_hours,
        password_min_length=settings.password_min_length,
    )


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    blacklist: TokenBlacklist = Depends(get_token_blacklist),
    config: AuthConfig = Depends(get_auth_config),
) -> AuthService:
    repo = UserRepository(session)
    return AuthService(user_repo=repo, token_blacklist=blacklist, config=config)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
) -> User:
    if token is None:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Not authenticated"})

    from app.domain.auth.exceptions import AuthenticationError

    try:
        payload = Token.decode(token, settings.jwt_secret_key, settings.jwt_algorithm)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": e.message}) from e

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Invalid token type"})

    blacklist = TokenBlacklist(redis)
    jti = payload.get("jti", "")
    if await blacklist.is_blacklisted(jti):
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "Token has been revoked"})

    repo = UserRepository(session)
    user = await repo.get_by_id(uuid.UUID(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail={"code": "INVALID_TOKEN", "message": "User not found"})
    if not user.is_active:
        raise HTTPException(status_code=403, detail={"code": "USER_INACTIVE", "message": "Account is inactive"})

    return user
