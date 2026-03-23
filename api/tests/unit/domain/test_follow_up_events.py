import dataclasses
import uuid

import pytest

from app.domain.follow_up.events import FollowUpCreated
from app.domain.shared.events import DomainEvent


class TestFollowUpCreated:
    def test_is_domain_event(self):
        event = FollowUpCreated(
            follow_up_id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
        )
        assert isinstance(event, DomainEvent)

    def test_frozen(self):
        event = FollowUpCreated(
            follow_up_id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
        )
        assert dataclasses.is_dataclass(event)
        with pytest.raises(dataclasses.FrozenInstanceError):
            event.follow_up_id = uuid.uuid7()  # type: ignore[misc]

    def test_has_event_id_and_occurred_at(self):
        event = FollowUpCreated(
            follow_up_id=uuid.uuid7(),
            customer_id=uuid.uuid7(),
        )
        assert isinstance(event.event_id, uuid.UUID)
        assert event.occurred_at is not None

    def test_follow_up_id_required(self):
        with pytest.raises(ValueError, match="follow_up_id"):
            FollowUpCreated(customer_id=uuid.uuid7())

    def test_customer_id_required(self):
        with pytest.raises(ValueError, match="customer_id"):
            FollowUpCreated(follow_up_id=uuid.uuid7())
