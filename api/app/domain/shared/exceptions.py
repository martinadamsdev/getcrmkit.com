class DomainError(Exception):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    def __init__(self, entity_type: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity_type} not found: {entity_id}",
            code="NOT_FOUND",
        )


class BusinessRuleViolationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="BUSINESS_RULE_VIOLATION")
