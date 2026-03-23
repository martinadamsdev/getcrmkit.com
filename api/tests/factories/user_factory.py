from app.domain.auth.entities import User
from app.domain.auth.value_objects import Email, Password


def make_user(
    email: str = "test@example.com",
    password: str = "Secure123",
    name: str = "Test User",
) -> User:
    return User.create(
        email=Email(email),
        password=Password.from_plain(password),
        name=name,
    )
