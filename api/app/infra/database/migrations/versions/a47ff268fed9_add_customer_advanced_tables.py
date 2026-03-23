"""add customer advanced tables

Revision ID: a47ff268fed9
Revises: 9d31846ed262
Create Date: 2026-03-23 06:50:18.975253

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "a47ff268fed9"
down_revision: str | Sequence[str] | None = "9d31846ed262"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "data_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("job_type", sa.String(length=20), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False),
        sa.Column("processed_rows", sa.Integer(), nullable=False),
        sa.Column("success_count", sa.Integer(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("result_file_url", sa.String(length=500), nullable=True),
        sa.Column("error_details", sa.JSON(), nullable=True),
        sa.Column("filter_config", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "saved_views",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("filter_config", sa.JSON(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # saved_views indexes
    op.create_index("idx_sv_user_entity_name", "saved_views", ["user_id", "entity_type", "name"], unique=True)
    op.create_index("idx_sv_user_entity", "saved_views", ["user_id", "entity_type"])

    # data_jobs indexes
    op.create_index("idx_dj_user_entity", "data_jobs", ["user_id", "entity_type"])
    op.create_index(
        "idx_dj_status", "data_jobs", ["status"], postgresql_where=text("status IN ('pending', 'processing')")
    )

    # contacts email domain index (for duplicate checking)
    op.execute(
        "CREATE INDEX idx_contact_domain ON contacts((split_part(email, '@', 2))) WHERE email IS NOT NULL AND deleted_at IS NULL"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS idx_contact_domain")
    op.drop_index("idx_dj_status", table_name="data_jobs")
    op.drop_index("idx_dj_user_entity", table_name="data_jobs")
    op.drop_index("idx_sv_user_entity", table_name="saved_views")
    op.drop_index("idx_sv_user_entity_name", table_name="saved_views")
    op.drop_table("saved_views")
    op.drop_table("data_jobs")
