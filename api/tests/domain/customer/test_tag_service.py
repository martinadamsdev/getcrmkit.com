import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import Tag
from app.domain.customer.exceptions import DuplicateTagError, TagNotFoundError
from app.domain.customer.repository import AbstractTagRepository
from app.domain.customer.services import TagService


@pytest.fixture
def mock_tag_repo():
    return AsyncMock(spec=AbstractTagRepository)


@pytest.fixture
def tag_service(mock_tag_repo):
    return TagService(tag_repo=mock_tag_repo)


class TestTagService:
    async def test_create_tag_success(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        created_by = uuid.uuid7()
        mock_tag_repo.get_by_name_and_group.return_value = None
        mock_tag_repo.create.return_value = Tag(name="VIP", tenant_id=uid)
        result = await tag_service.create_tag(
            name="VIP", group_name=None, color="#FF0000", position=0, tenant_id=uid, created_by=created_by,
        )
        assert result.name == "VIP"

    async def test_create_tag_duplicate_raises(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        created_by = uuid.uuid7()
        mock_tag_repo.get_by_name_and_group.return_value = Tag(name="VIP")
        with pytest.raises(DuplicateTagError):
            await tag_service.create_tag(
                name="VIP", group_name=None, color="#FF0000", position=0, tenant_id=uid, created_by=created_by,
            )

    async def test_update_tag_success(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        tag_id = uuid.uuid7()
        existing = Tag(name="Old", tenant_id=uid)
        updated = Tag(name="New", tenant_id=uid)
        mock_tag_repo.get_by_id.return_value = existing
        mock_tag_repo.update.return_value = updated
        result = await tag_service.update_tag(tenant_id=uid, tag_id=tag_id, name="New")
        assert result.name == "New"

    async def test_delete_tag_success(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        tag_id = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = Tag(name="Old")
        await tag_service.delete_tag(tenant_id=uid, tag_id=tag_id)
        mock_tag_repo.delete.assert_called_once_with(uid, tag_id)

    async def test_tag_customer_success(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        tag_id = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = Tag(name="VIP")
        await tag_service.tag_customer(tenant_id=uid, customer_id=customer_id, tag_id=tag_id)
        mock_tag_repo.add_to_customer.assert_called_once_with(uid, customer_id, tag_id)

    async def test_tag_customer_tag_not_found(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = None
        with pytest.raises(TagNotFoundError):
            await tag_service.tag_customer(tenant_id=uid, customer_id=uuid.uuid7(), tag_id=uuid.uuid7())

    async def test_tag_customer_idempotent(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = Tag(name="VIP")
        # Call twice — should not raise, add_to_customer called twice (idempotency at DB level)
        await tag_service.tag_customer(tenant_id=uid, customer_id=uuid.uuid7(), tag_id=uuid.uuid7())
        await tag_service.tag_customer(tenant_id=uid, customer_id=uuid.uuid7(), tag_id=uuid.uuid7())
        assert mock_tag_repo.add_to_customer.call_count == 2

    async def test_untag_customer_success(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        customer_id = uuid.uuid7()
        tag_id = uuid.uuid7()
        await tag_service.untag_customer(tenant_id=uid, customer_id=customer_id, tag_id=tag_id)
        mock_tag_repo.remove_from_customer.assert_called_once_with(uid, customer_id, tag_id)

    async def test_update_tag_not_found(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = None
        with pytest.raises(TagNotFoundError):
            await tag_service.update_tag(tenant_id=uid, tag_id=uuid.uuid7(), name="X")

    async def test_delete_tag_not_found(self, tag_service, mock_tag_repo):
        uid = uuid.uuid7()
        mock_tag_repo.get_by_id.return_value = None
        with pytest.raises(TagNotFoundError):
            await tag_service.delete_tag(tenant_id=uid, tag_id=uuid.uuid7())
