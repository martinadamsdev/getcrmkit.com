import uuid
from unittest.mock import AsyncMock

import pytest

from app.domain.follow_up.entities import FollowUp, ScriptTemplate
from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.domain.follow_up.exceptions import (
    FollowUpNotFoundError,
    ScriptTemplateNotFoundError,
    SystemTemplateCannotBeDeletedError,
)
from app.domain.follow_up.services import FollowUpService, ScriptTemplateService


class TestFollowUpService:
    def setup_method(self):
        self.repo = AsyncMock()
        self.service = FollowUpService(follow_up_repo=self.repo)

    async def test_create_follow_up(self):
        uid = uuid.uuid7()
        self.repo.create.return_value = FollowUp.create(
            customer_id=uid,
            method=FollowUpMethod.EMAIL,
            content="Test",
            tenant_id=uid,
            created_by=uid,
        )
        result = await self.service.create_follow_up(
            customer_id=uid,
            method=FollowUpMethod.EMAIL,
            content="Test",
            tenant_id=uid,
            created_by=uid,
        )
        assert result.content == "Test"
        self.repo.create.assert_awaited_once()

    async def test_get_follow_up_not_found(self):
        self.repo.get_by_id.return_value = None
        uid = uuid.uuid7()
        with pytest.raises(FollowUpNotFoundError):
            await self.service.get_follow_up(tenant_id=uid, follow_up_id=uid)

    async def test_get_follow_up_success(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid,
            method=FollowUpMethod.PHONE,
            content="Called",
            tenant_id=uid,
            created_by=uid,
        )
        self.repo.get_by_id.return_value = follow_up
        result = await self.service.get_follow_up(tenant_id=uid, follow_up_id=follow_up.id)
        assert result.content == "Called"

    async def test_update_follow_up_not_found(self):
        self.repo.get_by_id.return_value = None
        uid = uuid.uuid7()
        with pytest.raises(FollowUpNotFoundError):
            await self.service.update_follow_up(
                tenant_id=uid,
                follow_up_id=uid,
                content="Updated",
            )

    async def test_update_follow_up_success(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid,
            method=FollowUpMethod.EMAIL,
            content="Original",
            tenant_id=uid,
            created_by=uid,
        )
        self.repo.get_by_id.return_value = follow_up
        self.repo.update.return_value = follow_up
        await self.service.update_follow_up(
            tenant_id=uid,
            follow_up_id=follow_up.id,
            content="Updated",
        )
        self.repo.update.assert_awaited_once()

    async def test_soft_delete_not_found(self):
        self.repo.get_by_id.return_value = None
        uid = uuid.uuid7()
        with pytest.raises(FollowUpNotFoundError):
            await self.service.soft_delete_follow_up(tenant_id=uid, follow_up_id=uid)

    async def test_soft_delete_success(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid,
            method=FollowUpMethod.PHONE,
            content="Call",
            tenant_id=uid,
            created_by=uid,
        )
        self.repo.get_by_id.return_value = follow_up
        await self.service.soft_delete_follow_up(tenant_id=uid, follow_up_id=follow_up.id)
        self.repo.soft_delete.assert_awaited_once_with(uid, follow_up.id)

    async def test_list_by_customer(self):
        uid = uuid.uuid7()
        self.repo.get_by_customer_id.return_value = ([], 0)
        items, total = await self.service.list_by_customer(
            tenant_id=uid,
            customer_id=uid,
        )
        assert items == []
        assert total == 0

    async def test_list_by_tenant(self):
        uid = uuid.uuid7()
        self.repo.get_by_tenant.return_value = ([], 0)
        items, total = await self.service.list_by_tenant(tenant_id=uid)
        assert items == []
        assert total == 0


class TestScriptTemplateService:
    def setup_method(self):
        self.repo = AsyncMock()
        self.service = ScriptTemplateService(template_repo=self.repo)

    async def test_create_template(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.FIRST_CONTACT,
            title="Test",
            content="Content",
            tenant_id=uid,
        )
        self.repo.create.return_value = tpl
        result = await self.service.create_template(
            scene=ScriptScene.FIRST_CONTACT,
            title="Test",
            content="Content",
            tenant_id=uid,
        )
        assert result.title == "Test"
        self.repo.create.assert_awaited_once()

    async def test_update_template_not_found(self):
        self.repo.get_by_id.return_value = None
        uid = uuid.uuid7()
        with pytest.raises(ScriptTemplateNotFoundError):
            await self.service.update_template(
                tenant_id=uid,
                template_id=uid,
                title="Updated",
            )

    async def test_delete_template_not_found(self):
        self.repo.get_by_id.return_value = None
        uid = uuid.uuid7()
        with pytest.raises(ScriptTemplateNotFoundError):
            await self.service.delete_template(tenant_id=uid, template_id=uid)

    async def test_delete_system_template_raises(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.FIRST_CONTACT,
            title="System",
            content="Content",
            tenant_id=uid,
            is_system=True,
        )
        self.repo.get_by_id.return_value = tpl
        with pytest.raises(SystemTemplateCannotBeDeletedError):
            await self.service.delete_template(tenant_id=uid, template_id=tpl.id)

    async def test_delete_user_template_success(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.FOLLOW_UP,
            title="My Template",
            content="Content",
            tenant_id=uid,
        )
        self.repo.get_by_id.return_value = tpl
        await self.service.delete_template(tenant_id=uid, template_id=tpl.id)
        self.repo.delete.assert_awaited_once_with(uid, tpl.id)

    async def test_get_all(self):
        uid = uuid.uuid7()
        self.repo.get_all.return_value = []
        result = await self.service.get_all(tenant_id=uid)
        assert result == []
