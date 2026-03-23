import uuid

from app.domain.customer.entities import SavedView


class TestSavedView:
    def test_create_with_defaults(self):
        view = SavedView(user_id=uuid.uuid7())
        assert view.entity_type == "customer"
        assert view.name == ""
        assert view.filter_config == {}
        assert view.is_default is False
        assert view.position == 0

    def test_create_with_values(self):
        uid = uuid.uuid7()
        config = {"keyword": "acme", "source": "alibaba"}
        view = SavedView(
            user_id=uid, entity_type="customer", name="VIP Alibaba", filter_config=config, is_default=True, position=1
        )
        assert view.user_id == uid
        assert view.name == "VIP Alibaba"
        assert view.filter_config == config
        assert view.is_default is True
        assert view.position == 1

    def test_inherits_base_entity(self):
        view = SavedView(user_id=uuid.uuid7())
        assert view.id is not None
        assert view.tenant_id is not None
        assert view.created_at is not None
