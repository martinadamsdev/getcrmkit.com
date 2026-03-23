import uuid

import pytest

from app.domain.product.events import ProductCreated, ProductDeleted


class TestProductCreated:
    def test_creation(self):
        pid = uuid.uuid7()
        tid = uuid.uuid7()
        e = ProductCreated(product_id=pid, tenant_id=tid)
        assert e.product_id == pid
        assert e.tenant_id == tid
        assert e.event_id is not None
        assert e.occurred_at is not None

    def test_frozen(self):
        e = ProductCreated(product_id=uuid.uuid7(), tenant_id=uuid.uuid7())
        with pytest.raises(AttributeError):
            e.product_id = uuid.uuid7()  # type: ignore[misc]

    def test_product_id_required(self):
        with pytest.raises(ValueError, match="product_id"):
            ProductCreated(product_id=None, tenant_id=uuid.uuid7())  # type: ignore[arg-type]

    def test_tenant_id_none_allowed(self):
        e = ProductCreated(product_id=uuid.uuid7(), tenant_id=None)  # type: ignore[arg-type]
        assert e.tenant_id is None

    def test_created_by_field(self):
        pid = uuid.uuid7()
        tid = uuid.uuid7()
        uid = uuid.uuid7()
        e = ProductCreated(product_id=pid, tenant_id=tid, created_by=uid)
        assert e.created_by == uid


class TestProductDeleted:
    def test_creation(self):
        pid = uuid.uuid7()
        tid = uuid.uuid7()
        e = ProductDeleted(product_id=pid, tenant_id=tid)
        assert e.product_id == pid
        assert e.tenant_id == tid

    def test_product_id_required(self):
        with pytest.raises(ValueError, match="product_id"):
            ProductDeleted(product_id=None, tenant_id=uuid.uuid7())  # type: ignore[arg-type]

    def test_tenant_id_none_allowed(self):
        e = ProductDeleted(product_id=uuid.uuid7(), tenant_id=None)  # type: ignore[arg-type]
        assert e.tenant_id is None
