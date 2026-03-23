import uuid
from unittest.mock import AsyncMock

import pytest

from app.application.customer.queries import Customer360QueryService
from app.domain.customer.entities import Contact, Customer, CustomerGrade, Tag
from app.domain.customer.exceptions import CustomerNotFoundError


def _customer(grade_id=None):
    return Customer(name="Test", tenant_id=uuid.uuid7(), created_by=uuid.uuid7(), grade_id=grade_id)


def _grade():
    return CustomerGrade(name="A", tenant_id=uuid.uuid7())


@pytest.fixture
def repos():
    return {
        "customer_repo": AsyncMock(),
        "contact_repo": AsyncMock(),
        "grade_repo": AsyncMock(),
        "tag_repo": AsyncMock(),
    }


class TestCustomer360QueryService:
    async def test_full_view(self, repos):
        grade = _grade()
        customer = _customer(grade_id=grade.id)
        contact = Contact(customer_id=customer.id, name="John", tenant_id=customer.tenant_id)
        repos["customer_repo"].get_by_id.return_value = customer
        repos["grade_repo"].get_by_id.return_value = grade
        repos["tag_repo"].get_by_customer_id.return_value = [Tag(name="VIP", tenant_id=customer.tenant_id)]
        repos["contact_repo"].get_by_customer_id.return_value = [contact]
        svc = Customer360QueryService(**repos)
        view = await svc.get_360_view(customer.id, customer.tenant_id)
        assert view.customer.name == "Test"
        assert view.grade is not None
        assert view.grade.name == "A"
        assert len(view.contacts) == 1
        assert len(view.tags) == 1
        assert view.follow_ups == []
        assert view.quotations == []
        assert view.orders == []
        assert view.stats.contact_count == 1
        assert view.stats.follow_up_count == 0

    async def test_no_grade(self, repos):
        customer = _customer()
        repos["customer_repo"].get_by_id.return_value = customer
        repos["contact_repo"].get_by_customer_id.return_value = []
        repos["tag_repo"].get_by_customer_id.return_value = []
        svc = Customer360QueryService(**repos)
        view = await svc.get_360_view(customer.id, customer.tenant_id)
        assert view.grade is None

    async def test_customer_not_found(self, repos):
        repos["customer_repo"].get_by_id.return_value = None
        svc = Customer360QueryService(**repos)
        with pytest.raises(CustomerNotFoundError):
            await svc.get_360_view(uuid.uuid7(), uuid.uuid7())
