import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.domain.follow_up.entities import FollowUp
from app.domain.follow_up.enums import FollowUpMethod


class TestReminderHandler:
    @pytest.fixture
    def follow_up_repo(self):
        return AsyncMock()

    @pytest.fixture
    def notification_repo(self):
        return AsyncMock()

    @pytest.fixture
    def handler(self, follow_up_repo, notification_repo):
        from app.application.follow_up.commands import ReminderHandler

        return ReminderHandler(
            follow_up_repo=follow_up_repo,
            notification_repo=notification_repo,
        )

    async def test_due_follow_ups_creates_notifications(
        self, handler, follow_up_repo, notification_repo
    ):
        tenant_id = uuid.uuid7()
        user_id = uuid.uuid7()
        fu = FollowUp(
            id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
            content="Test follow up",
            method=FollowUpMethod.EMAIL,
            tenant_id=tenant_id,
            created_by=user_id,
            next_follow_at=datetime.now(UTC) - timedelta(hours=1),
        )

        follow_up_repo.find_due_reminders.return_value = [fu]
        follow_up_repo.update.return_value = fu

        count = await handler.check_and_notify()

        assert count == 1
        notification_repo.create.assert_called_once()
        call_kwargs = notification_repo.create.call_args[1]
        assert call_kwargs["tenant_id"] == tenant_id
        assert call_kwargs["user_id"] == user_id
        assert call_kwargs["type"] == "follow_up_reminder"
        assert call_kwargs["ref_type"] == "follow_up"
        assert call_kwargs["ref_id"] == fu.id

        # next_follow_at should be cleared
        follow_up_repo.update.assert_called_once()
        updated_fu = follow_up_repo.update.call_args[0][0]
        assert updated_fu.next_follow_at is None

    async def test_no_due_follow_ups_returns_zero(
        self, handler, follow_up_repo, notification_repo
    ):
        follow_up_repo.find_due_reminders.return_value = []

        count = await handler.check_and_notify()

        assert count == 0
        notification_repo.create.assert_not_called()

    async def test_skips_deleted_follow_ups(
        self, handler, follow_up_repo, notification_repo
    ):
        """Deleted follow-ups (deleted_at set) should be skipped by is_reminder_due."""
        fu = FollowUp(
            id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
            content="Deleted follow up",
            method=FollowUpMethod.PHONE,
            tenant_id=uuid.uuid7(),
            created_by=uuid.uuid7(),
            next_follow_at=datetime.now(UTC) - timedelta(hours=1),
            deleted_at=datetime.now(UTC),
        )

        follow_up_repo.find_due_reminders.return_value = [fu]

        count = await handler.check_and_notify()

        assert count == 0
        notification_repo.create.assert_not_called()

    async def test_clears_next_follow_at_after_notification(
        self, handler, follow_up_repo, notification_repo
    ):
        fu = FollowUp(
            id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
            content="Follow up",
            method=FollowUpMethod.WECHAT,
            tenant_id=uuid.uuid7(),
            created_by=uuid.uuid7(),
            next_follow_at=datetime.now(UTC) - timedelta(minutes=30),
        )

        follow_up_repo.find_due_reminders.return_value = [fu]
        follow_up_repo.update.return_value = fu

        await handler.check_and_notify()

        # Verify next_follow_at was cleared
        updated_fu = follow_up_repo.update.call_args[0][0]
        assert updated_fu.next_follow_at is None

    async def test_multiple_due_follow_ups(
        self, handler, follow_up_repo, notification_repo
    ):
        fus = []
        for _ in range(3):
            fu = FollowUp(
                id=uuid.uuid7(),
                customer_id=uuid.uuid7(),
                content="Follow up",
                method=FollowUpMethod.EMAIL,
                tenant_id=uuid.uuid7(),
                created_by=uuid.uuid7(),
                next_follow_at=datetime.now(UTC) - timedelta(hours=2),
            )
            fus.append(fu)

        follow_up_repo.find_due_reminders.return_value = fus
        follow_up_repo.update.side_effect = lambda fu: fu

        count = await handler.check_and_notify()

        assert count == 3
        assert notification_repo.create.call_count == 3
        assert follow_up_repo.update.call_count == 3
