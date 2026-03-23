import uuid
from decimal import Decimal

import pytest

from app.domain.product.entities import Product, ProductCategory
from app.domain.product.events import ProductCreated
from app.domain.product.exceptions import MaxCategoryDepthError, ProductNameRequiredError


class TestProduct:
    def test_create_minimal(self):
        tid = uuid.uuid7()
        uid = uuid.uuid7()
        p = Product.create(name="Widget", tenant_id=tid, created_by=uid)
        assert p.name == "Widget"
        assert p.tenant_id == tid
        assert p.created_by == uid
        assert p.sku is None
        assert p.is_active is True
        assert p.cost_price is None
        assert p.cost_currency == "CNY"
        assert p.selling_price is None
        assert p.selling_currency == "USD"
        assert p.custom_fields == {}

    def test_create_full(self):
        tid = uuid.uuid7()
        uid = uuid.uuid7()
        cat_id = uuid.uuid7()
        p = Product.create(
            name="Gadget Pro",
            tenant_id=tid,
            created_by=uid,
            sku="GP-001",
            category_id=cat_id,
            description="A fine gadget",
            image_url="https://example.com/img.jpg",
            material="Stainless Steel",
            dimensions="10x5x3 cm",
            weight=Decimal("0.250"),
            color="Silver",
            packing="Box + Foam",
            cost_price=Decimal("45.5000"),
            cost_currency="CNY",
            selling_price=Decimal("12.9900"),
            selling_currency="USD",
            is_active=True,
            custom_fields={"moq": 100},
        )
        assert p.sku == "GP-001"
        assert p.category_id == cat_id
        assert p.cost_price == Decimal("45.5000")
        assert p.selling_price == Decimal("12.9900")
        assert p.custom_fields == {"moq": 100}

    def test_create_empty_name_raises(self):
        with pytest.raises(ProductNameRequiredError):
            Product.create(name="", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())

    def test_create_whitespace_name_raises(self):
        with pytest.raises(ProductNameRequiredError):
            Product.create(name="   ", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())

    def test_create_strips_name(self):
        p = Product.create(name="  Widget  ", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        assert p.name == "Widget"

    def test_create_emits_event(self):
        p = Product.create(name="Widget", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        events = p.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], ProductCreated)
        assert events[0].product_id == p.id
        assert events[0].tenant_id == p.tenant_id

    def test_inherits_base_entity(self):
        p = Product.create(name="X", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        assert p.id is not None
        assert p.created_at is not None
        assert p.deleted_at is None
        assert p.is_deleted is False

    def test_soft_delete(self):
        p = Product.create(name="X", tenant_id=uuid.uuid7(), created_by=uuid.uuid7())
        p.soft_delete()
        assert p.is_deleted is True


class TestProductCategory:
    def test_create_root(self):
        tid = uuid.uuid7()
        cat = ProductCategory(name="Electronics", tenant_id=tid)
        assert cat.name == "Electronics"
        assert cat.parent_id is None
        assert cat.level == 1
        assert cat.position == 0

    def test_create_child(self):
        parent_id = uuid.uuid7()
        cat = ProductCategory(name="Phones", parent_id=parent_id, level=2, tenant_id=uuid.uuid7())
        assert cat.parent_id == parent_id
        assert cat.level == 2

    def test_create_grandchild(self):
        cat = ProductCategory(name="Smartphones", parent_id=uuid.uuid7(), level=3, tenant_id=uuid.uuid7())
        assert cat.level == 3

    def test_validate_max_depth_raises(self):
        cat = ProductCategory(name="Too Deep", parent_id=uuid.uuid7(), level=4, tenant_id=uuid.uuid7())
        with pytest.raises(MaxCategoryDepthError):
            cat.validate_depth()

    def test_validate_depth_ok(self):
        cat = ProductCategory(name="OK", level=3, tenant_id=uuid.uuid7())
        cat.validate_depth()  # should not raise
