import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import SavedView
from app.domain.customer.exceptions import DuplicateViewNameError, SavedViewNotFoundError
from app.domain.customer.services import SavedViewService


@pytest.fixture
def repo():
    r = AsyncMock()
    r.get_by_name = AsyncMock(return_value=None)
    r.get_by_id = AsyncMock(return_value=None)
    r.create = AsyncMock(side_effect=lambda v: v)
    r.update = AsyncMock(side_effect=lambda v: v)
    r.delete = AsyncMock()
    r.get_all = AsyncMock(return_value=[])
    return r


class TestSavedViewService:
    async def test_create_success(self, repo):
        svc = SavedViewService(repo)
        view = await svc.create_view(
            tenant_id=uuid.uuid7(),
            user_id=uuid.uuid7(),
            name="My Filter",
            entity_type="customer",
            filter_config={"source": "alibaba"},
        )
        assert view.name == "My Filter"
        repo.create.assert_called_once()

    async def test_create_duplicate_name_raises(self, repo):
        repo.get_by_name.return_value = SavedView(user_id=uuid.uuid7(), name="My Filter")
        svc = SavedViewService(repo)
        with pytest.raises(DuplicateViewNameError):
            await svc.create_view(
                tenant_id=uuid.uuid7(), user_id=uuid.uuid7(), name="My Filter", entity_type="customer", filter_config={}
            )

    async def test_update_success(self, repo):
        existing = SavedView(user_id=uuid.uuid7(), name="Old Name")
        repo.get_by_id.return_value = existing
        svc = SavedViewService(repo)
        result = await svc.update_view(
            id=existing.id, tenant_id=existing.tenant_id, user_id=existing.user_id, name="New Name"
        )
        assert result.name == "New Name"

    async def test_update_not_found_raises(self, repo):
        svc = SavedViewService(repo)
        with pytest.raises(SavedViewNotFoundError):
            await svc.update_view(id=uuid.uuid7(), tenant_id=uuid.uuid7(), user_id=uuid.uuid7(), name="X")

    async def test_update_duplicate_name_raises(self, repo):
        existing = SavedView(user_id=uuid.uuid7(), name="Old Name")
        repo.get_by_id.return_value = existing
        repo.get_by_name.return_value = SavedView(user_id=existing.user_id, name="Taken Name")
        svc = SavedViewService(repo)
        with pytest.raises(DuplicateViewNameError):
            await svc.update_view(
                id=existing.id, tenant_id=existing.tenant_id, user_id=existing.user_id, name="Taken Name"
            )

    async def test_delete_not_found_raises(self, repo):
        svc = SavedViewService(repo)
        with pytest.raises(SavedViewNotFoundError):
            await svc.delete_view(id=uuid.uuid7(), tenant_id=uuid.uuid7(), user_id=uuid.uuid7())
