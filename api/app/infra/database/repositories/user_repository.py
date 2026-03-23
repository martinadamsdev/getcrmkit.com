import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.entities import User
from app.domain.auth.repository import AbstractUserRepository
from app.domain.auth.value_objects import Email
from app.infra.database.models.user import UserModel


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.email = user.email.value
        model.password_hash = user.password_hash
        model.name = user.name
        model.timezone = user.timezone
        model.language = user.language
        model.role = user.role
        model.is_active = user.is_active
        model.last_login_at = user.last_login_at
        model.updated_at = user.updated_at
        model.updated_by = user.updated_by
        await self._session.flush()
        return self._to_entity(model)

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(UserModel.id).where(
            UserModel.email == email,
            UserModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            tenant_id=user.tenant_id,
            email=user.email.value,
            password_hash=user.password_hash,
            name=user.name,
            timezone=user.timezone,
            language=user.language,
            role=user.role,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
            created_by=user.created_by,
            updated_by=user.updated_by,
        )

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            tenant_id=model.tenant_id,
            email=Email(model.email),
            password_hash=model.password_hash,
            name=model.name,
            timezone=model.timezone,
            language=model.language,
            role=model.role,
            is_active=model.is_active,
            last_login_at=model.last_login_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
