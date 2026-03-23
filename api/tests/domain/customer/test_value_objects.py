import uuid
from datetime import UTC, datetime

from app.domain.customer.enums import FollowUpStage
from app.domain.customer.value_objects import Customer360Stats, CustomerFilter, DuplicateMatch


class TestCustomerFilter:
    def test_default_values(self):
        f = CustomerFilter()
        assert f.keyword is None
        assert f.grade_id is None
        assert f.source is None
        assert f.follow_status is None
        assert f.country is None
        assert f.industry is None
        assert f.tag_ids == []
        assert f.owner_id is None
        assert f.created_at_from is None
        assert f.created_at_to is None
        assert f.last_follow_at_from is None
        assert f.last_follow_at_to is None
        assert f.sort_by == "created_at"
        assert f.sort == "desc"

    def test_frozen_immutable(self):
        f = CustomerFilter()
        import pytest

        with pytest.raises(AttributeError):
            f.keyword = "test"  # type: ignore[misc]

    def test_with_all_fields(self):
        grade_id = uuid.uuid7()
        tag_id = uuid.uuid7()
        owner_id = uuid.uuid7()
        now = datetime.now(UTC)
        f = CustomerFilter(
            keyword="acme",
            grade_id=grade_id,
            source="alibaba",
            follow_status=FollowUpStage.NEW,
            country="US",
            industry="Electronics",
            tag_ids=[tag_id],
            owner_id=owner_id,
            created_at_from=now,
            created_at_to=now,
            last_follow_at_from=now,
            last_follow_at_to=now,
            sort_by="name",
            sort="asc",
        )
        assert f.keyword == "acme"
        assert f.grade_id == grade_id
        assert f.tag_ids == [tag_id]
        assert f.sort_by == "name"
        assert f.sort == "asc"


class TestDuplicateMatch:
    def test_creation(self):
        cid = uuid.uuid7()
        m = DuplicateMatch(
            customer_id=cid,
            customer_name="Acme Corp",
            match_type="name_exact",
            matched_value="Acme Corp",
        )
        assert m.customer_id == cid
        assert m.match_type == "name_exact"

    def test_frozen(self):
        import pytest

        m = DuplicateMatch(customer_id=uuid.uuid7(), customer_name="X", match_type="name_exact", matched_value="X")
        with pytest.raises(AttributeError):
            m.customer_name = "Y"  # type: ignore[misc]


class TestCustomer360Stats:
    def test_defaults(self):
        s = Customer360Stats(contact_count=3)
        assert s.contact_count == 3
        assert s.follow_up_count == 0
        assert s.quotation_count == 0
        assert s.order_count == 0
        assert s.last_follow_at is None
        assert s.total_order_amount is None
