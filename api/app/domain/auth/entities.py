import uuid
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.auth.value_objects import Email, Password
from app.domain.shared.entity import BaseEntity


@dataclass
class User(BaseEntity):
    email: Email = field(default_factory=lambda: Email("placeholder@example.com"))
    password_hash: str = ""
    name: str = ""
    timezone: str = "Asia/Shanghai"
    language: str = "zh-CN"
    role: str = "owner"
    is_active: bool = True
    last_login_at: datetime | None = None

    @classmethod
    def create(
        cls,
        email: Email,
        password: Password,
        name: str,
    ) -> User:
        user_id = uuid.uuid7()
        return cls(
            id=user_id,
            tenant_id=user_id,
            email=email,
            password_hash=password.hashed,
            name=name,
            created_by=None,
        )
