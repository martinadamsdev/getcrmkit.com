import uuid
from datetime import UTC, datetime, timedelta

import pytest

from app.domain.follow_up.entities import FollowUp, ScriptTemplate
from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.domain.follow_up.exceptions import FollowUpContentRequiredError, ScriptTemplateTitleRequiredError


class TestFollowUp:
    def test_create_factory(self):
        tenant_id = uuid.uuid7()
        customer_id = uuid.uuid7()
        user_id = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=customer_id,
            method=FollowUpMethod.EMAIL,
            content="Sent quotation via email",
            tenant_id=tenant_id,
            created_by=user_id,
        )
        assert follow_up.customer_id == customer_id
        assert follow_up.method == FollowUpMethod.EMAIL
        assert follow_up.content == "Sent quotation via email"
        assert isinstance(follow_up.id, uuid.UUID)

    def test_create_requires_content(self):
        uid = uuid.uuid7()
        with pytest.raises(FollowUpContentRequiredError):
            FollowUp.create(
                customer_id=uid,
                method=FollowUpMethod.PHONE,
                content="",
                tenant_id=uid,
                created_by=uid,
            )

    def test_create_strips_whitespace_only_content(self):
        uid = uuid.uuid7()
        with pytest.raises(FollowUpContentRequiredError):
            FollowUp.create(
                customer_id=uid,
                method=FollowUpMethod.PHONE,
                content="   ",
                tenant_id=uid,
                created_by=uid,
            )

    def test_tags_default_empty(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.WECHAT,
            content="Hello", tenant_id=uid, created_by=uid,
        )
        assert follow_up.tags == []

    def test_tags_assigned(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.WECHAT,
            content="Hello", tenant_id=uid, created_by=uid,
            tags=["urgent", "vip"],
        )
        assert follow_up.tags == ["urgent", "vip"]

    def test_next_follow_at_optional(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.PHONE,
            content="Call", tenant_id=uid, created_by=uid,
        )
        assert follow_up.next_follow_at is None

    def test_is_reminder_due_true(self):
        uid = uuid.uuid7()
        past = datetime.now(UTC) - timedelta(hours=1)
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.PHONE,
            content="Call", tenant_id=uid, created_by=uid,
            next_follow_at=past,
        )
        assert follow_up.is_reminder_due is True

    def test_is_reminder_due_false_future(self):
        uid = uuid.uuid7()
        future = datetime.now(UTC) + timedelta(hours=1)
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.PHONE,
            content="Call", tenant_id=uid, created_by=uid,
            next_follow_at=future,
        )
        assert follow_up.is_reminder_due is False

    def test_is_reminder_due_false_no_reminder(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.PHONE,
            content="Call", tenant_id=uid, created_by=uid,
        )
        assert follow_up.is_reminder_due is False

    def test_create_emits_follow_up_created_event(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.EMAIL,
            content="Test", tenant_id=uid, created_by=uid,
        )
        events = follow_up.pull_events()
        assert len(events) == 1
        from app.domain.follow_up.events import FollowUpCreated
        assert isinstance(events[0], FollowUpCreated)
        assert events[0].follow_up_id == follow_up.id
        assert events[0].customer_id == uid

    def test_attachment_urls_default_empty(self):
        uid = uuid.uuid7()
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.EMAIL,
            content="Test", tenant_id=uid, created_by=uid,
        )
        assert follow_up.attachment_urls == []

    def test_is_reminder_due_false_when_deleted(self):
        uid = uuid.uuid7()
        past = datetime.now(UTC) - timedelta(hours=1)
        follow_up = FollowUp.create(
            customer_id=uid, method=FollowUpMethod.PHONE,
            content="Call", tenant_id=uid, created_by=uid,
            next_follow_at=past,
        )
        follow_up.soft_delete()
        assert follow_up.is_reminder_due is False


class TestScriptTemplate:
    def test_create_factory(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.FIRST_CONTACT,
            title="Initial Contact Script",
            content="Hello, we are...",
            tenant_id=uid,
        )
        assert tpl.title == "Initial Contact Script"
        assert tpl.scene == ScriptScene.FIRST_CONTACT
        assert tpl.is_system is False

    def test_create_title_required(self):
        uid = uuid.uuid7()
        with pytest.raises(ScriptTemplateTitleRequiredError):
            ScriptTemplate.create(
                scene=ScriptScene.FOLLOW_UP,
                title="",
                content="Some content",
                tenant_id=uid,
            )

    def test_create_title_whitespace_only(self):
        uid = uuid.uuid7()
        with pytest.raises(ScriptTemplateTitleRequiredError):
            ScriptTemplate.create(
                scene=ScriptScene.FOLLOW_UP,
                title="   ",
                content="Some content",
                tenant_id=uid,
            )

    def test_system_template(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.FIRST_CONTACT,
            title="System Template",
            content="Template content",
            tenant_id=uid,
            is_system=True,
        )
        assert tpl.is_system is True

    def test_default_language(self):
        uid = uuid.uuid7()
        tpl = ScriptTemplate.create(
            scene=ScriptScene.QUOTATION,
            title="Quote Script",
            content="Content",
            tenant_id=uid,
        )
        assert tpl.language == "zh-CN"
