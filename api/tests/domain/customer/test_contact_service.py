import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import Contact, Customer
from app.domain.customer.exceptions import ContactNotFoundError, CustomerNotFoundError
from app.domain.customer.repository import AbstractContactRepository, AbstractCustomerRepository
from app.domain.customer.services import ContactService


@pytest.fixture
def mock_contact_repo():
    return AsyncMock(spec=AbstractContactRepository)


@pytest.fixture
def mock_customer_repo():
    return AsyncMock(spec=AbstractCustomerRepository)


@pytest.fixture
def contact_service(mock_contact_repo, mock_customer_repo):
    return ContactService(contact_repo=mock_contact_repo, customer_repo=mock_customer_repo)


class TestContactService:
    async def test_create_contact_success(self, contact_service, mock_contact_repo, mock_customer_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = Customer(name="Acme", tenant_id=uid)
        mock_contact_repo.get_by_customer_id.return_value = []
        contact = Contact(customer_id=customer_id, name="John")
        mock_contact_repo.create.return_value = contact
        result = await contact_service.create_contact(
            customer_id=customer_id, name="John", tenant_id=uid, created_by=uid,
        )
        assert result.name == "John"

    async def test_create_contact_customer_not_found(self, contact_service, mock_customer_repo):
        uid = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = None
        with pytest.raises(CustomerNotFoundError):
            await contact_service.create_contact(
                customer_id=uuid.uuid7(), name="John", tenant_id=uid, created_by=uid,
            )

    async def test_create_first_contact_auto_primary(self, contact_service, mock_contact_repo, mock_customer_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = Customer(name="Acme", tenant_id=uid)
        mock_contact_repo.get_by_customer_id.return_value = []  # no existing contacts
        captured = {}
        async def capture(contact):
            captured["is_primary"] = contact.is_primary
            return contact
        mock_contact_repo.create.side_effect = capture
        await contact_service.create_contact(
            customer_id=customer_id, name="First", tenant_id=uid, created_by=uid,
        )
        assert captured["is_primary"] is True

    async def test_set_primary_success(self, contact_service, mock_contact_repo):
        uid = uuid.uuid7()
        contact_id = uuid.uuid7()
        customer_id = uuid.uuid7()
        contact = Contact(customer_id=customer_id, name="John", is_primary=False)
        contact.id = contact_id
        mock_contact_repo.get_by_id.return_value = contact
        mock_contact_repo.update.return_value = contact
        await contact_service.set_primary(tenant_id=uid, contact_id=contact_id)
        mock_contact_repo.clear_primary.assert_called_once_with(uid, customer_id)

    async def test_set_primary_contact_not_found(self, contact_service, mock_contact_repo):
        uid = uuid.uuid7()
        mock_contact_repo.get_by_id.return_value = None
        with pytest.raises(ContactNotFoundError):
            await contact_service.set_primary(tenant_id=uid, contact_id=uuid.uuid7())

    async def test_soft_delete_contact_success(self, contact_service, mock_contact_repo):
        uid = uuid.uuid7()
        contact_id = uuid.uuid7()
        mock_contact_repo.get_by_id.return_value = Contact(customer_id=uuid.uuid7(), name="John")
        await contact_service.soft_delete_contact(tenant_id=uid, contact_id=contact_id)
        mock_contact_repo.soft_delete.assert_called_once_with(uid, contact_id)

    async def test_soft_delete_contact_not_found(self, contact_service, mock_contact_repo):
        uid = uuid.uuid7()
        mock_contact_repo.get_by_id.return_value = None
        with pytest.raises(ContactNotFoundError):
            await contact_service.soft_delete_contact(tenant_id=uid, contact_id=uuid.uuid7())

    async def test_create_contact_second_not_auto_primary(
        self, contact_service, mock_contact_repo, mock_customer_repo
    ):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        mock_customer_repo.get_by_id.return_value = Customer(name="Acme", tenant_id=uid)
        # Simulate one existing contact already present
        existing_contact = Contact(customer_id=customer_id, name="First")
        mock_contact_repo.get_by_customer_id.return_value = [existing_contact]
        captured = {}

        async def capture(contact):
            captured["is_primary"] = contact.is_primary
            return contact

        mock_contact_repo.create.side_effect = capture
        await contact_service.create_contact(
            customer_id=customer_id, name="Second", tenant_id=uid, created_by=uid,
        )
        assert captured["is_primary"] is False
