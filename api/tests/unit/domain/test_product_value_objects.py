from decimal import Decimal

import pytest

from app.domain.product.value_objects import ProductFilter
from app.domain.shared.value_objects import Money


class TestMoney:
    """Money already exists in domain/shared/value_objects.py — verify import works."""

    def test_default_cny(self):
        m = Money(amount=Decimal("99.50"))
        assert m.amount == Decimal("99.50")
        assert m.currency == "CNY"

    def test_usd(self):
        m = Money(amount=Decimal("12.00"), currency="USD")
        assert m.currency == "USD"

    def test_frozen_immutable(self):
        m = Money(amount=Decimal("1.00"))
        with pytest.raises(AttributeError):
            m.amount = Decimal("2.00")  # type: ignore[misc]

    def test_zero_amount(self):
        m = Money(amount=Decimal("0"))
        assert m.amount == Decimal("0")

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(amount=Decimal("-1.00"))

    def test_equality(self):
        a = Money(amount=Decimal("10.00"), currency="CNY")
        b = Money(amount=Decimal("10.00"), currency="CNY")
        assert a == b

    def test_different_currency_not_equal(self):
        a = Money(amount=Decimal("10.00"), currency="CNY")
        b = Money(amount=Decimal("10.00"), currency="USD")
        assert a != b


class TestProductFilter:
    def test_default_values(self):
        f = ProductFilter()
        assert f.keyword is None
        assert f.category_id is None
        assert f.is_active is None
        assert f.min_cost is None
        assert f.max_cost is None
        assert f.min_selling is None
        assert f.max_selling is None
        assert f.sort_by == "created_at"
        assert f.sort == "desc"

    def test_frozen_immutable(self):
        f = ProductFilter()
        with pytest.raises(AttributeError):
            f.keyword = "test"  # type: ignore[misc]

    def test_with_all_fields(self):
        import uuid

        cat_id = uuid.uuid7()
        f = ProductFilter(
            keyword="widget",
            category_id=cat_id,
            is_active=True,
            min_cost=Decimal("10.00"),
            max_cost=Decimal("100.00"),
            min_selling=Decimal("15.00"),
            max_selling=Decimal("150.00"),
            sort_by="name",
            sort="asc",
        )
        assert f.keyword == "widget"
        assert f.category_id == cat_id
        assert f.is_active is True
        assert f.min_cost == Decimal("10.00")
        assert f.min_selling == Decimal("15.00")
        assert f.sort_by == "name"
        assert f.sort == "asc"
