from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.shared.unit_of_work import AbstractUnitOfWork
from app.infra.database.connection import async_session_factory


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_factory

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        self.session: AsyncSession = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
