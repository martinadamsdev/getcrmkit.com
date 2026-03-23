import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import PricingTier
from app.infra.database.repositories.pricing_tier_repository import PricingTierRepository


@pytest.fixture
def tenant_id():
    return uuid.uuid7()


@pytest.fixture
def tier_repo(db_session: AsyncSession):
    return PricingTierRepository(db_session)


def _make_tier(tenant_id: uuid.UUID, **kwargs) -> PricingTier:
    now = datetime.now(UTC)
    defaults = {
        "name": "Small Order",
        "min_qty": 1,
        "max_qty": 99,
        "multiplier": Decimal("1.5000"),
        "is_default": False,
        "position": 0,
    }
    defaults.update(kwargs)
    return PricingTier(
        tenant_id=tenant_id,
        created_at=now,
        updated_at=now,
        **defaults,
    )


class TestPricingTierRepository:
    async def test_create_and_get_by_id(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        tier = _make_tier(tenant_id)
        created = await tier_repo.create(tier)
        result = await tier_repo.get_by_id(tenant_id, created.id)
        assert result is not None
        assert result.name == "Small Order"
        assert result.multiplier == Decimal("1.5000")

    async def test_get_by_id_not_found(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        result = await tier_repo.get_by_id(tenant_id, uuid.uuid7())
        assert result is None

    async def test_get_all_sorted_by_position(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        await tier_repo.create(_make_tier(tenant_id, name="Large", position=2, min_qty=1000))
        await tier_repo.create(_make_tier(tenant_id, name="Small", position=0, min_qty=1))
        await tier_repo.create(_make_tier(tenant_id, name="Medium", position=1, min_qty=100))
        tiers = await tier_repo.get_all(tenant_id)
        assert len(tiers) == 3
        assert [t.name for t in tiers] == ["Small", "Medium", "Large"]

    async def test_update(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        tier = await tier_repo.create(_make_tier(tenant_id))
        tier.name = "Updated Name"
        tier.multiplier = Decimal("2.0000")
        tier.updated_at = datetime.now(UTC)
        updated = await tier_repo.update(tier)
        assert updated.name == "Updated Name"
        assert updated.multiplier == Decimal("2.0000")

    async def test_delete(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        tier = await tier_repo.create(_make_tier(tenant_id))
        await tier_repo.delete(tenant_id, tier.id)
        result = await tier_repo.get_by_id(tenant_id, tier.id)
        assert result is None

    async def test_tenant_isolation(self, tier_repo: PricingTierRepository, tenant_id: uuid.UUID) -> None:
        other_tenant = uuid.uuid7()
        await tier_repo.create(_make_tier(tenant_id, name="Mine"))
        await tier_repo.create(_make_tier(other_tenant, name="Other"))
        tiers = await tier_repo.get_all(tenant_id)
        assert len(tiers) == 1
        assert tiers[0].name == "Mine"
