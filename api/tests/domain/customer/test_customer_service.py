import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import Customer
from app.domain.customer.events import CustomerGradeChanged
from app.domain.customer.exceptions import CustomerNameRequiredError, CustomerNotFoundError
from app.domain.customer.repository import AbstractCustomerRepository
from app.domain.customer.services import CustomerService


@pytest.fixture
def mock_customer_repo():
    return AsyncMock(spec=AbstractCustomerRepository)


@pytest.fixture
def customer_service(mock_customer_repo):
    return CustomerService(customer_repo=mock_customer_repo)


def make_customer(name: str = "Acme", **kwargs) -> Customer:
    uid = uuid.uuid7()
    return Customer(name=name, tenant_id=uid, created_by=uid, **kwargs)


class TestCustomerService:
    async def test_create_customer_success(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        mock_customer_repo.create.return_value = make_customer("Acme")
        result = await customer_service.create_customer(
            name="Acme", tenant_id=uid, created_by=uid, owner_id=uid,
        )
        mock_customer_repo.create.assert_called_once()
        assert result.name == "Acme"

    async def test_create_customer_name_empty_raises(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        with pytest.raises(CustomerNameRequiredError):
            await customer_service.create_customer(name="", tenant_id=uid, created_by=uid, owner_id=uid)

    async def test_create_customer_auto_owner_id(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        captured = {}
        async def capture_create(customer):
            captured["owner_id"] = customer.owner_id
            return customer
        mock_customer_repo.create.side_effect = capture_create
        await customer_service.create_customer(name="Test", tenant_id=uid, created_by=uid, owner_id=uid)
        assert captured["owner_id"] == uid

    async def test_update_customer_success(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        existing = make_customer("Old Name")
        updated = make_customer("New Name")
        mock_customer_repo.get_by_id.return_value = existing
        mock_customer_repo.update.return_value = updated
        result = await customer_service.update_customer(
            tenant_id=uid, customer_id=customer_id, name="New Name",
        )
        assert result.name == "New Name"

    async def test_update_customer_not_found_raises(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = None
        with pytest.raises(CustomerNotFoundError):
            await customer_service.update_customer(tenant_id=uid, customer_id=uuid.uuid7(), name="X")

    async def test_soft_delete_customer_success(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = make_customer()
        await customer_service.soft_delete_customer(tenant_id=uid, customer_id=customer_id)
        mock_customer_repo.soft_delete.assert_called_once_with(uid, customer_id)

    async def test_soft_delete_customer_not_found(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = None
        with pytest.raises(CustomerNotFoundError):
            await customer_service.soft_delete_customer(tenant_id=uid, customer_id=uuid.uuid7())

    async def test_update_customer_grade_changed_emits_event(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        old_grade_id = uuid.uuid7()
        new_grade_id = uuid.uuid7()
        existing = make_customer(grade_id=old_grade_id)
        updated = make_customer(grade_id=new_grade_id)
        mock_customer_repo.get_by_id.return_value = existing
        mock_customer_repo.update.return_value = updated
        result = await customer_service.update_customer(
            tenant_id=uid, customer_id=uuid.uuid7(), grade_id=new_grade_id,
        )
        # Event should be recorded on the updated entity
        all_events = result.pull_events()
        events = [e for e in all_events if isinstance(e, CustomerGradeChanged)]
        assert len(events) == 1
        assert events[0].old_grade_id == old_grade_id
        assert events[0].new_grade_id == new_grade_id

    async def test_update_customer_grade_unchanged_no_event(self, customer_service, mock_customer_repo):
        uid = uuid.uuid7()
        grade_id = uuid.uuid7()
        existing = make_customer(grade_id=grade_id)
        updated = make_customer(grade_id=grade_id)
        mock_customer_repo.get_by_id.return_value = existing
        mock_customer_repo.update.return_value = updated
        result = await customer_service.update_customer(
            tenant_id=uid, customer_id=uuid.uuid7(), grade_id=grade_id,
        )
        all_events = result.pull_events()
        events = [e for e in all_events if isinstance(e, CustomerGradeChanged)]
        assert len(events) == 0
