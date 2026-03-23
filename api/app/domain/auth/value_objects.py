import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.domain.auth.exceptions import AuthenticationError, WeakPasswordError

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _EMAIL_REGEX.match(normalized):
            msg = f"Invalid email: {self.value}"
            raise ValueError(msg)
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Password:
    hashed: str

    @classmethod
    def from_plain(cls, plain: str, min_length: int = 8) -> Password:
        if len(plain) < min_length:
            raise WeakPasswordError(f"Password must be at least {min_length} characters")
        if not any(c.isalpha() for c in plain):
            raise WeakPasswordError("Password must contain at least one letter")
        if not any(c.isdigit() for c in plain):
            raise WeakPasswordError("Password must contain at least one digit")
        hashed = bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
        return cls(hashed=hashed)

    @classmethod
    def from_hash(cls, hashed: str) -> Password:
        return cls(hashed=hashed)

    def verify(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode(), self.hashed.encode())


@dataclass(frozen=True)
class Token:
    value: str
    jti: str

    @classmethod
    def create_access_token(
        cls,
        user_id: str,
        secret: str,
        algorithm: str,
        expire_minutes: int,
    ) -> Token:
        jti = str(uuid.uuid7())
        payload = {
            "sub": user_id,
            "type": "access",
            "jti": jti,
            "exp": datetime.now(UTC) + timedelta(minutes=expire_minutes),
            "iat": datetime.now(UTC),
        }
        value = jwt.encode(payload, secret, algorithm=algorithm)
        return cls(value=value, jti=jti)

    @classmethod
    def create_refresh_token(
        cls,
        user_id: str,
        secret: str,
        algorithm: str,
        expire_days: int | None = None,
        expire_hours: int | None = None,
        remember_me: bool = False,
    ) -> Token:
        jti = str(uuid.uuid7())
        if expire_days is not None:
            delta = timedelta(days=expire_days)
        elif expire_hours is not None:
            delta = timedelta(hours=expire_hours)
        else:
            msg = "Must provide expire_days or expire_hours"
            raise ValueError(msg)
        payload: dict[str, Any] = {
            "sub": user_id,
            "type": "refresh",
            "jti": jti,
            "exp": datetime.now(UTC) + delta,
            "iat": datetime.now(UTC),
            "remember_me": remember_me,
        }
        value = jwt.encode(payload, secret, algorithm=algorithm)
        return cls(value=value, jti=jti)

    @staticmethod
    def decode(token: str, secret: str, algorithm: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, secret, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired") from None
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token") from None


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
