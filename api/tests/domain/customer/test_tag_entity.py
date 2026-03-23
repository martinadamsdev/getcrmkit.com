from app.domain.customer.entities import Tag


class TestTag:
    def test_create_with_name(self):
        tag = Tag(name="VIP")
        assert tag.name == "VIP"

    def test_color_default_value(self):
        tag = Tag(name="Important")
        assert tag.color == "#3B82F6"

    def test_group_name_optional(self):
        tag = Tag(name="Region")
        assert tag.group_name is None
        assert tag.position == 0
