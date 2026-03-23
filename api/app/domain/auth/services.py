import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol, runtime_checkable

from app.domain.auth.entities import User
from app.domain.auth.exceptions import (
    AuthenticationError,
    DuplicateEmailError,
    UserInactiveError,
    UserNotFoundError,
)
from app.domain.auth.repository import AbstractUserRepository
from app.domain.auth.value_objects import Email, Password, Token, TokenPair


@dataclass(frozen=True)
class AuthConfig:
    """Pure dataclass — no framework dependency in domain layer."""

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    refresh_token_short_expire_hours: int = 24
    password_min_length: int = 8


@runtime_checkable
class TokenBlacklistProtocol(Protocol):
    async def add(self, jti: str, ttl: int) -> None: ...
    async def is_blacklisted(self, jti: str) -> bool: ...


class AuthService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        token_blacklist: TokenBlacklistProtocol,
        config: AuthConfig,
    ) -> None:
        self._repo = user_repo
        self._blacklist = token_blacklist
        self._config = config

    async def register(self, email: str, password: str, name: str) -> User:
        email_vo = Email(email)
        if await self._repo.exists_by_email(email_vo.value):
            raise DuplicateEmailError(email_vo.value)

        password_vo = Password.from_plain(password, min_length=self._config.password_min_length)
        user = User.create(email=email_vo, password=password_vo, name=name)
        return await self._repo.create(user)

    async def login(
        self,
        email: str,
        password: str,
        remember_me: bool = False,
    ) -> TokenPair:
        user = await self._repo.get_by_email(email.strip().lower())
        if user is None:
            raise AuthenticationError()

        if not user.is_active:
            raise UserInactiveError()

        pw = Password.from_hash(user.password_hash)
        if not pw.verify(password):
            raise AuthenticationError()

        user.last_login_at = datetime.now(UTC)
        await self._repo.update(user)

        return self._create_token_pair(str(user.id), remember_me)

    async def refresh(self, refresh_token: str) -> TokenPair:
        payload = Token.decode(
            refresh_token,
            self._config.jwt_secret_key,
            self._config.jwt_algorithm,
        )
        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type")

        jti = payload.get("jti", "")
        if await self._blacklist.is_blacklisted(jti):
            raise AuthenticationError("Token has been revoked")

        exp = payload.get("exp", 0)
        await self._blacklist.add(jti, ttl=max(0, int(exp - datetime.now(UTC).timestamp())))

        remember_me = payload.get("remember_me", False)
        return self._create_token_pair(payload["sub"], remember_me=remember_me)

    async def logout(self, access_token: str, refresh_token: str) -> None:
        c = self._config
        for token_str in (access_token, refresh_token):
            if not token_str:
                continue
            try:
                payload = Token.decode(token_str, c.jwt_secret_key, c.jwt_algorithm)
                jti = payload.get("jti", "")
                exp = payload.get("exp", 0)
                ttl = max(0, int(exp - datetime.now(UTC).timestamp()))
                await self._blacklist.add(jti, ttl=ttl)
            except AuthenticationError:
                pass

    async def get_profile(self, user_id: uuid.UUID) -> User:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(str(user_id))
        return user

    async def update_profile(
        self,
        user_id: uuid.UUID,
        name: str | None = None,
        timezone: str | None = None,
        language: str | None = None,
    ) -> User:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(str(user_id))

        if name is not None:
            user.name = name
        if timezone is not None:
            user.timezone = timezone
        if language is not None:
            user.language = language
        user.updated_by = user_id

        return await self._repo.update(user)

    async def change_password(
        self,
        user_id: uuid.UUID,
        old_password: str,
        new_password: str,
    ) -> None:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(str(user_id))

        pw = Password.from_hash(user.password_hash)
        if not pw.verify(old_password):
            raise AuthenticationError("Current password is incorrect")

        new_pw = Password.from_plain(new_password, min_length=self._config.password_min_length)
        user.password_hash = new_pw.hashed
        user.updated_by = user_id
        await self._repo.update(user)

    def _create_token_pair(self, user_id: str, remember_me: bool) -> TokenPair:
        c = self._config
        access = Token.create_access_token(
            user_id=user_id,
            secret=c.jwt_secret_key,
            algorithm=c.jwt_algorithm,
            expire_minutes=c.access_token_expire_minutes,
        )
        if remember_me:
            refresh = Token.create_refresh_token(
                user_id=user_id,
                secret=c.jwt_secret_key,
                algorithm=c.jwt_algorithm,
                expire_days=c.refresh_token_expire_days,
                remember_me=True,
            )
        else:
            refresh = Token.create_refresh_token(
                user_id=user_id,
                secret=c.jwt_secret_key,
                algorithm=c.jwt_algorithm,
                expire_hours=c.refresh_token_short_expire_hours,
                remember_me=False,
            )
        return TokenPair(
            access_token=access.value,
            refresh_token=refresh.value,
            expires_in=c.access_token_expire_minutes * 60,
        )
