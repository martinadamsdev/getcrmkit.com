from app.domain.shared.exceptions import DomainError


class AuthenticationError(DomainError):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message=message, code="INVALID_CREDENTIALS")


class DuplicateEmailError(DomainError):
    def __init__(self, email: str) -> None:
        super().__init__(
            message=f"Email already registered: {email}",
            code="DUPLICATE_EMAIL",
        )


class UserNotFoundError(DomainError):
    def __init__(self, user_id: str) -> None:
        super().__init__(
            message=f"User not found: {user_id}",
            code="USER_NOT_FOUND",
        )


class UserInactiveError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="User account is inactive",
            code="USER_INACTIVE",
        )


class WeakPasswordError(DomainError):
    def __init__(self, reason: str) -> None:
        super().__init__(
            message=f"Password too weak: {reason}",
            code="WEAK_PASSWORD",
        )
