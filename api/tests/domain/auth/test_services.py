import time
from unittest.mock import AsyncMock

import pytest

from app.domain.auth.entities import User
from app.domain.auth.exceptions import (
    AuthenticationError,
    DuplicateEmailError,
)
from app.domain.auth.repository import AbstractUserRepository
from app.domain.auth.services import AuthConfig, AuthService
from app.domain.auth.value_objects import Email, Password, Token


def _make_config(**overrides) -> AuthConfig:
    defaults = {
        "jwt_secret_key": "test-secret",
        "jwt_algorithm": "HS256",
        "access_token_expire_minutes": 60,
        "refresh_token_expire_days": 30,
        "refresh_token_short_expire_hours": 24,
        "password_min_length": 8,
    }
    defaults.update(overrides)
    return AuthConfig(**defaults)


def _make_user(email: str = "test@example.com", password: str = "Secure123") -> User:
    return User.create(
        email=Email(email),
        password=Password.from_plain(password),
        name="Test User",
    )


@pytest.fixture
def mock_repo():
    return AsyncMock(spec=AbstractUserRepository)


@pytest.fixture
def mock_blacklist():
    return AsyncMock()


@pytest.fixture
def config():
    return _make_config()


@pytest.fixture
def auth_service(mock_repo, mock_blacklist, config):
    return AuthService(
        user_repo=mock_repo,
        token_blacklist=mock_blacklist,
        config=config,
    )


class TestRegister:
    async def test_register_success(self, auth_service, mock_repo):
        mock_repo.exists_by_email.return_value = False
        mock_repo.create.side_effect = lambda user: user

        user = await auth_service.register("new@example.com", "Secure123", "New User")

        assert user.email.value == "new@example.com"
        assert user.name == "New User"
        assert user.tenant_id == user.id
        mock_repo.create.assert_called_once()

    async def test_register_duplicate_email(self, auth_service, mock_repo):
        mock_repo.exists_by_email.return_value = True

        with pytest.raises(DuplicateEmailError):
            await auth_service.register("taken@example.com", "Secure123", "User")


class TestLogin:
    async def test_login_success(self, auth_service, mock_repo):
        user = _make_user()
        mock_repo.get_by_email.return_value = user
        mock_repo.update.side_effect = lambda u: u

        pair = await auth_service.login("test@example.com", "Secure123")

        assert pair.access_token
        assert pair.refresh_token
        assert pair.token_type == "bearer"

    async def test_login_wrong_password(self, auth_service, mock_repo):
        user = _make_user()
        mock_repo.get_by_email.return_value = user

        with pytest.raises(AuthenticationError):
            await auth_service.login("test@example.com", "wrong")

    async def test_login_nonexistent_email(self, auth_service, mock_repo):
        mock_repo.get_by_email.return_value = None

        with pytest.raises(AuthenticationError):
            await auth_service.login("nobody@example.com", "Secure123")

    async def test_login_remember_me_long_ttl(self, auth_service, mock_repo, config):
        user = _make_user()
        mock_repo.get_by_email.return_value = user
        mock_repo.update.side_effect = lambda u: u

        pair = await auth_service.login("test@example.com", "Secure123", remember_me=True)
        payload = Token.decode(pair.refresh_token, config.jwt_secret_key, config.jwt_algorithm)
        assert payload["exp"] - time.time() > 29 * 86400
        assert payload["remember_me"] is True

    async def test_login_no_remember_me_short_ttl(self, auth_service, mock_repo, config):
        user = _make_user()
        mock_repo.get_by_email.return_value = user
        mock_repo.update.side_effect = lambda u: u

        pair = await auth_service.login("test@example.com", "Secure123", remember_me=False)
        payload = Token.decode(pair.refresh_token, config.jwt_secret_key, config.jwt_algorithm)
        assert payload["exp"] - time.time() < 25 * 3600
        assert payload["remember_me"] is False
