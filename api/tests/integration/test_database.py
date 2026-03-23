import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_database_version(db_session: AsyncSession):
    result = await db_session.execute(text("SELECT version()"))
    version = result.scalar()
    assert "PostgreSQL" in version
