from app.domain.shared.exceptions import DomainError


class FollowUpContentRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Follow-up content is required",
            code="FOLLOW_UP_CONTENT_REQUIRED",
        )


class FollowUpNotFoundError(DomainError):
    def __init__(self, follow_up_id: str) -> None:
        super().__init__(
            message=f"Follow-up not found: {follow_up_id}",
            code="FOLLOW_UP_NOT_FOUND",
        )


class ScriptTemplateNotFoundError(DomainError):
    def __init__(self, template_id: str) -> None:
        super().__init__(
            message=f"Script template not found: {template_id}",
            code="SCRIPT_TEMPLATE_NOT_FOUND",
        )


class ScriptTemplateTitleRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Script template title is required",
            code="SCRIPT_TEMPLATE_TITLE_REQUIRED",
        )


class SystemTemplateCannotBeDeletedError(DomainError):
    def __init__(self, template_id: str) -> None:
        super().__init__(
            message=f"System template cannot be deleted: {template_id}",
            code="SYSTEM_TEMPLATE_PROTECTED",
        )
