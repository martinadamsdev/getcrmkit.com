import uuid

import pytest

from app.domain.customer.entities import Customer
from app.domain.customer.enums import FollowUpStage
from app.domain.customer.exceptions import CustomerNameRequiredError


class TestCustomer:
    def test_create_with_required_name(self):
        customer_id = uuid.uuid7()
        customer = Customer.create(
            name="Acme Corp",
            tenant_id=customer_id,
            created_by=customer_id,
        )
        assert customer.name == "Acme Corp"
        assert isinstance(customer.id, uuid.UUID)

    def test_default_follow_status_is_new(self):
        uid = uuid.uuid7()
        customer = Customer.create(name="Test", tenant_id=uid, created_by=uid)
        assert customer.follow_status == FollowUpStage.NEW

    def test_grade_id_optional(self):
        uid = uuid.uuid7()
        customer = Customer.create(name="Test", tenant_id=uid, created_by=uid)
        assert customer.grade_id is None

    def test_custom_fields_default_empty_dict(self):
        uid = uuid.uuid7()
        customer = Customer.create(name="Test", tenant_id=uid, created_by=uid)
        assert customer.custom_fields == {}

    def test_soft_delete_sets_deleted_at(self):
        uid = uuid.uuid7()
        customer = Customer.create(name="Test", tenant_id=uid, created_by=uid)
        assert not customer.is_deleted
        customer.soft_delete()
        assert customer.is_deleted

    def test_create_factory_validates_name(self):
        uid = uuid.uuid7()
        with pytest.raises(CustomerNameRequiredError):
            Customer.create(name="", tenant_id=uid, created_by=uid)
        with pytest.raises(CustomerNameRequiredError):
            Customer.create(name="   ", tenant_id=uid, created_by=uid)
