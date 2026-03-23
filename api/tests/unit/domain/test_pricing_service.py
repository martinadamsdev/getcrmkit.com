import uuid
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.domain.product.entities import PricingTier
from app.domain.product.services import PricingService


def _tier(min_qty: int, max_qty: int | None, multiplier: str, name: str = "") -> PricingTier:
    return PricingTier(
        name=name,
        min_qty=min_qty,
        max_qty=max_qty,
        multiplier=Decimal(multiplier),
        tenant_id=uuid.uuid7(),
    )


@pytest.fixture
def tier_repo():
    repo = AsyncMock()
    repo.get_all = AsyncMock(return_value=[])
    return repo


class TestPricingService:
    async def test_get_multiplier_first_tier(self, tier_repo):
        tier_repo.get_all.return_value = [
            _tier(1, 99, "1.5000", "Retail"),
            _tier(100, 499, "1.3600", "Wholesale"),
            _tier(500, None, "1.2000", "Bulk"),
        ]
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=50)
        assert result == Decimal("1.5000")

    async def test_get_multiplier_middle_tier(self, tier_repo):
        tier_repo.get_all.return_value = [
            _tier(1, 99, "1.5000"),
            _tier(100, 499, "1.3600"),
            _tier(500, None, "1.2000"),
        ]
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=250)
        assert result == Decimal("1.3600")

    async def test_get_multiplier_open_ended_tier(self, tier_repo):
        """AC-0.6.2: PricingService.get_multiplier(250) returns 100-499 tier multiplier."""
        tier_repo.get_all.return_value = [
            _tier(1, 99, "1.5000"),
            _tier(100, 499, "1.3600"),
            _tier(500, None, "1.2000"),
        ]
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=1000)
        assert result == Decimal("1.2000")

    async def test_get_multiplier_exact_boundary(self, tier_repo):
        tier_repo.get_all.return_value = [
            _tier(1, 99, "1.5000"),
            _tier(100, 499, "1.3600"),
        ]
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=100)
        assert result == Decimal("1.3600")

    async def test_get_multiplier_no_tiers_returns_default(self, tier_repo):
        """No tiers defined -> return 1.0000 (original price)."""
        tier_repo.get_all.return_value = []
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=10)
        assert result == Decimal("1.0000")

    async def test_get_multiplier_qty_below_all_tiers_returns_default(self, tier_repo):
        """Quantity below all tier ranges -> return 1.0000 (original price)."""
        tier_repo.get_all.return_value = [
            _tier(100, 499, "1.3600"),
        ]
        svc = PricingService(pricing_tier_repo=tier_repo)
        result = await svc.get_multiplier(tenant_id=uuid.uuid7(), qty=5)
        assert result == Decimal("1.0000")
