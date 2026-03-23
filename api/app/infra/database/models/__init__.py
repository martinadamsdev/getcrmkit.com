from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover them
from app.infra.database.models.user import UserModel  # noqa: E402, F401
