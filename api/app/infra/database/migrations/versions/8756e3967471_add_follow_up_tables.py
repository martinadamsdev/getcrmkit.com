"""add follow_up tables

Revision ID: 8756e3967471
Revises: a47ff268fed9
Create Date: 2026-03-23 11:57:45.501200

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8756e3967471"
down_revision: str | Sequence[str] | None = "a47ff268fed9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- follow_ups ---
    op.create_table(
        "follow_ups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("contact_id", sa.Uuid(), nullable=True),
        sa.Column("method", sa.String(length=20), nullable=False),
        sa.Column("stage", sa.String(length=20), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("customer_response", sa.Text(), nullable=True),
        sa.Column("next_follow_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attachment_urls", sa.ARRAY(sa.Text()), nullable=False),
        sa.Column("tags", sa.ARRAY(sa.Text()), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["contact_id"], ["contacts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_follow_ups_tenant_customer",
        "follow_ups",
        ["tenant_id", "customer_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_follow_ups_next_follow_at",
        "follow_ups",
        ["next_follow_at"],
        postgresql_where=sa.text("next_follow_at IS NOT NULL AND deleted_at IS NULL"),
    )
    op.create_index(
        "idx_follow_ups_tenant_created_by",
        "follow_ups",
        ["tenant_id", "created_by"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_follow_ups_tags",
        "follow_ups",
        ["tags"],
        postgresql_using="gin",
    )

    # --- script_templates ---
    op.create_table(
        "script_templates",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("scene", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_system", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- notifications (stub) ---
    op.create_table(
        "notifications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("ref_type", sa.String(length=50), nullable=True),
        sa.Column("ref_id", sa.Uuid(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_notifications_tenant_user_read",
        "notifications",
        ["tenant_id", "user_id", "is_read"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_notifications_tenant_user_read", table_name="notifications")
    op.drop_table("notifications")
    op.drop_table("script_templates")
    op.drop_index("idx_follow_ups_tags", table_name="follow_ups", postgresql_using="gin")
    op.drop_index("idx_follow_ups_tenant_created_by", table_name="follow_ups")
    op.drop_index("idx_follow_ups_next_follow_at", table_name="follow_ups")
    op.drop_index("idx_follow_ups_tenant_customer", table_name="follow_ups")
    op.drop_table("follow_ups")
