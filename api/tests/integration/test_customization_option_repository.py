import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import CustomizationOption
from app.infra.database.repositories.customization_option_repository import CustomizationOptionRepository


@pytest.fixture
def tenant_id():
    return uuid.uuid7()


@pytest.fixture
def option_repo(db_session: AsyncSession):
    return CustomizationOptionRepository(db_session)


def _make_option(tenant_id: uuid.UUID, **kwargs) -> CustomizationOption:
    defaults = {
        "name": "Logo Printing",
        "description": "Custom logo on product",
        "extra_cost": Decimal("5.00"),
        "extra_currency": "CNY",
        "is_active": True,
    }
    defaults.update(kwargs)
    return CustomizationOption.create(tenant_id=tenant_id, **defaults)


class TestCustomizationOptionRepository:
    async def test_create_and_get_by_id(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        option = _make_option(tenant_id)
        created = await option_repo.create(option)
        result = await option_repo.get_by_id(tenant_id, created.id)
        assert result is not None
        assert result.name == "Logo Printing"
        assert result.extra_cost == Decimal("5.00")

    async def test_get_by_id_not_found(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        result = await option_repo.get_by_id(tenant_id, uuid.uuid7())
        assert result is None

    async def test_get_all(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        await option_repo.create(_make_option(tenant_id, name="Option A"))
        await option_repo.create(_make_option(tenant_id, name="Option B"))
        options = await option_repo.get_all(tenant_id)
        assert len(options) == 2

    async def test_update(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        option = await option_repo.create(_make_option(tenant_id))
        option.name = "Updated Logo"
        option.extra_cost = Decimal("10.00")
        option.updated_at = datetime.now(UTC)
        updated = await option_repo.update(option)
        assert updated.name == "Updated Logo"
        assert updated.extra_cost == Decimal("10.00")

    async def test_delete(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        option = await option_repo.create(_make_option(tenant_id))
        await option_repo.delete(tenant_id, option.id)
        result = await option_repo.get_by_id(tenant_id, option.id)
        assert result is None

    async def test_tenant_isolation(self, option_repo: CustomizationOptionRepository, tenant_id: uuid.UUID) -> None:
        other_tenant = uuid.uuid7()
        await option_repo.create(_make_option(tenant_id, name="Mine"))
        await option_repo.create(_make_option(other_tenant, name="Other"))
        options = await option_repo.get_all(tenant_id)
        assert len(options) == 1
        assert options[0].name == "Mine"
