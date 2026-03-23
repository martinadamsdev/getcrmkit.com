import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import CustomerGrade
from app.domain.customer.exceptions import CustomerGradeNotFoundError, GradeInUseError
from app.domain.customer.repository import AbstractCustomerGradeRepository, AbstractCustomerRepository
from app.domain.customer.services import CustomerGradeService


@pytest.fixture
def mock_grade_repo():
    return AsyncMock(spec=AbstractCustomerGradeRepository)


@pytest.fixture
def mock_customer_repo():
    return AsyncMock(spec=AbstractCustomerRepository)


@pytest.fixture
def grade_service(mock_grade_repo, mock_customer_repo):
    return CustomerGradeService(grade_repo=mock_grade_repo, customer_repo=mock_customer_repo)


class TestCustomerGradeService:
    async def test_create_grade_success(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        created_by = uuid.uuid7()
        mock_grade = CustomerGrade(name="S", tenant_id=tenant_id)
        mock_grade_repo.create.return_value = mock_grade
        result = await grade_service.create_grade(
            name="S",
            label="超级VIP",
            color="#FF0000",
            position=0,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        mock_grade_repo.create.assert_called_once()
        assert result.name == "S"

    async def test_update_grade_success(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grade_id = uuid.uuid7()
        existing = CustomerGrade(name="A", tenant_id=tenant_id)
        existing.id = grade_id
        updated = CustomerGrade(name="AA", tenant_id=tenant_id)
        mock_grade_repo.get_by_id.return_value = existing
        mock_grade_repo.update.return_value = updated
        result = await grade_service.update_grade(tenant_id=tenant_id, grade_id=grade_id, name="AA")
        assert result.name == "AA"

    async def test_delete_grade_success(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grade_id = uuid.uuid7()
        mock_grade_repo.get_by_id.return_value = CustomerGrade(name="A", tenant_id=tenant_id)
        mock_grade_repo.has_customers.return_value = False
        await grade_service.delete_grade(tenant_id=tenant_id, grade_id=grade_id)
        mock_grade_repo.delete.assert_called_once_with(tenant_id, grade_id)

    async def test_delete_grade_in_use_raises(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grade_id = uuid.uuid7()
        mock_grade_repo.get_by_id.return_value = CustomerGrade(name="A", tenant_id=tenant_id)
        mock_grade_repo.has_customers.return_value = True
        with pytest.raises(GradeInUseError):
            await grade_service.delete_grade(tenant_id=tenant_id, grade_id=grade_id)

    async def test_get_all_returns_list(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grades = [CustomerGrade(name="A"), CustomerGrade(name="B")]
        mock_grade_repo.get_all.return_value = grades
        result = await grade_service.get_all(tenant_id=tenant_id)
        assert len(result) == 2

    async def test_update_grade_not_found(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grade_id = uuid.uuid7()
        mock_grade_repo.get_by_id.return_value = None
        with pytest.raises(CustomerGradeNotFoundError):
            await grade_service.update_grade(tenant_id=tenant_id, grade_id=grade_id, name="X")

    async def test_delete_grade_not_found(self, grade_service, mock_grade_repo):
        tenant_id = uuid.uuid7()
        grade_id = uuid.uuid7()
        mock_grade_repo.get_by_id.return_value = None
        with pytest.raises(CustomerGradeNotFoundError):
            await grade_service.delete_grade(tenant_id=tenant_id, grade_id=grade_id)
