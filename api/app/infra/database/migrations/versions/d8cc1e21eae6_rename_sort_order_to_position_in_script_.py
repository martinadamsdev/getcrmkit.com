"""rename sort_order to position in script_templates

Revision ID: d8cc1e21eae6
Revises: 8756e3967471
Create Date: 2026-03-23 21:13:27.946249

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8cc1e21eae6"
down_revision: str | Sequence[str] | None = "8756e3967471"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename sort_order → position for naming consistency with customer domain."""
    op.alter_column("script_templates", "sort_order", new_column_name="position")


def downgrade() -> None:
    """Revert position → sort_order."""
    op.alter_column("script_templates", "position", new_column_name="sort_order")
