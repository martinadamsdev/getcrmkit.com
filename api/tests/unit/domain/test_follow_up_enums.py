import pytest

from app.domain.follow_up.enums import FollowUpMethod, ScriptScene


class TestFollowUpMethod:
    def test_all_values(self):
        expected = {
            "phone", "email", "wechat", "whatsapp",
            "alibaba", "meeting", "exhibition", "other",
        }
        assert {m.value for m in FollowUpMethod} == expected

    def test_is_str_enum(self):
        assert isinstance(FollowUpMethod.EMAIL, str)
        assert FollowUpMethod.ALIBABA == "alibaba"

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            FollowUpMethod("telegram")


class TestScriptScene:
    def test_all_values(self):
        expected = {
            "first_contact", "follow_up", "quotation", "sample",
            "order_confirm", "after_sales", "reactivation",
        }
        assert {s.value for s in ScriptScene} == expected

    def test_is_str_enum(self):
        assert isinstance(ScriptScene.FIRST_CONTACT, str)
        assert ScriptScene.FIRST_CONTACT == "first_contact"
