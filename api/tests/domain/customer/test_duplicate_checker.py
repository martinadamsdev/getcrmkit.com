import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import Customer
from app.domain.customer.services import DuplicateChecker


def _make_customer(name: str = "Acme Corp") -> Customer:
    return Customer(name=name, tenant_id=uuid.uuid7(), created_by=uuid.uuid7())


@pytest.fixture
def customer_repo():
    repo = AsyncMock()
    repo.find_by_name_exact = AsyncMock(return_value=[])
    repo.find_by_email_domain = AsyncMock(return_value=[])
    repo.find_by_email_exact = AsyncMock(return_value=[])
    return repo


class TestDuplicateChecker:
    async def test_name_exact_match(self, customer_repo):
        customer = _make_customer("ACME Corp")
        customer_repo.find_by_name_exact.return_value = [customer]
        checker = DuplicateChecker(customer_repo)
        result = await checker.check(tenant_id=uuid.uuid7(), name="Acme Corp")
        assert len(result) == 1
        assert result[0].match_type == "name_exact"
        assert result[0].customer_name == "ACME Corp"

    async def test_email_domain_match(self, customer_repo):
        customer = _make_customer("Acme Trading")
        customer_repo.find_by_email_domain.return_value = [customer]
        checker = DuplicateChecker(customer_repo)
        result = await checker.check(tenant_id=uuid.uuid7(), name="Other Co", email="john@acme.com")
        assert len(result) == 1
        assert result[0].match_type == "email_domain"
        assert result[0].matched_value == "acme.com"

    async def test_email_exact_match(self, customer_repo):
        customer = _make_customer("Acme Inc")
        customer_repo.find_by_email_exact.return_value = [customer]
        checker = DuplicateChecker(customer_repo)
        result = await checker.check(tenant_id=uuid.uuid7(), name="Other Co", email="john@acme.com")
        assert any(m.match_type == "email_exact" for m in result)

    async def test_public_domain_skipped(self, customer_repo):
        checker = DuplicateChecker(customer_repo)
        await checker.check(tenant_id=uuid.uuid7(), name="No Match", email="user@gmail.com")
        customer_repo.find_by_email_domain.assert_not_called()

    async def test_no_duplicates(self, customer_repo):
        checker = DuplicateChecker(customer_repo)
        result = await checker.check(tenant_id=uuid.uuid7(), name="Unique Corp")
        assert result == []

    async def test_exclude_id_forwarded(self, customer_repo):
        checker = DuplicateChecker(customer_repo)
        exclude = uuid.uuid7()
        await checker.check(tenant_id=uuid.uuid7(), name="X", email="x@acme.com", exclude_id=exclude)
        customer_repo.find_by_name_exact.assert_called_once()
        assert customer_repo.find_by_name_exact.call_args[0][2] == exclude
        customer_repo.find_by_email_domain.assert_called_once()
        assert customer_repo.find_by_email_domain.call_args[0][2] == exclude
        customer_repo.find_by_email_exact.assert_called_once()
        assert customer_repo.find_by_email_exact.call_args[0][2] == exclude

    async def test_deduplication(self, customer_repo):
        customer = _make_customer("Acme Corp")
        customer_repo.find_by_name_exact.return_value = [customer]
        customer_repo.find_by_email_domain.return_value = [customer]
        checker = DuplicateChecker(customer_repo)
        result = await checker.check(tenant_id=uuid.uuid7(), name="Acme Corp", email="x@acme.com")
        customer_ids = [m.customer_id for m in result]
        assert len(set(customer_ids)) == len(customer_ids)
