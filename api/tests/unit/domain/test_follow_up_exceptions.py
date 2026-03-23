from app.domain.follow_up.exceptions import (
    FollowUpContentRequiredError,
    FollowUpNotFoundError,
    ScriptTemplateNotFoundError,
    ScriptTemplateTitleRequiredError,
    SystemTemplateCannotBeDeletedError,
)
from app.domain.shared.exceptions import DomainError


class TestFollowUpExceptions:
    def test_content_required_error(self):
        err = FollowUpContentRequiredError()
        assert isinstance(err, DomainError)
        assert err.code == "FOLLOW_UP_CONTENT_REQUIRED"

    def test_not_found_error(self):
        err = FollowUpNotFoundError("some-id")
        assert "some-id" in err.message
        assert err.code == "FOLLOW_UP_NOT_FOUND"

    def test_template_not_found_error(self):
        err = ScriptTemplateNotFoundError("tpl-id")
        assert "tpl-id" in err.message
        assert err.code == "SCRIPT_TEMPLATE_NOT_FOUND"

    def test_template_title_required_error(self):
        err = ScriptTemplateTitleRequiredError()
        assert isinstance(err, DomainError)
        assert err.code == "SCRIPT_TEMPLATE_TITLE_REQUIRED"

    def test_system_template_protected_error(self):
        err = SystemTemplateCannotBeDeletedError("sys-id")
        assert "sys-id" in err.message
        assert err.code == "SYSTEM_TEMPLATE_PROTECTED"
