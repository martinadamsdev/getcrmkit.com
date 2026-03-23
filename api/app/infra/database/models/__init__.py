from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover them
from app.infra.database.models.customer import (  # noqa: E402, F401
    ContactModel,
    CustomerGradeModel,
    CustomerModel,
    TagModel,
)
from app.infra.database.models.user import UserModel  # noqa: E402, F401
