"""add customer tables

Revision ID: 9d31846ed262
Revises: 5c899c658874
Create Date: 2026-03-23 04:30:41.545555

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d31846ed262"
down_revision: str | Sequence[str] | None = "5c899c658874"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "customer_grades",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("label", sa.String(length=200), nullable=True),
        sa.Column("color", sa.String(length=7), nullable=False, server_default="#3B82F6"),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "name", name="uq_customer_grades_tenant_name"),
    )

    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("region", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("company_size", sa.String(length=20), nullable=True),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=True),
        sa.Column("grade_id", sa.Uuid(), nullable=True),
        sa.Column("follow_status", sa.String(length=50), nullable=False, server_default="new"),
        sa.Column("main_products", sa.Text(), nullable=True),
        sa.Column("annual_volume", sa.String(length=100), nullable=True),
        sa.Column("current_supplier", sa.Text(), nullable=True),
        sa.Column("decision_process", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.Uuid(), nullable=True),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_follow_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("custom_fields", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["grade_id"], ["customer_grades.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "contacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("whatsapp", sa.String(length=50), nullable=True),
        sa.Column("skype", sa.String(length=100), nullable=True),
        sa.Column("linkedin", sa.String(length=500), nullable=True),
        sa.Column("wechat", sa.String(length=100), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("custom_fields", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("color", sa.String(length=7), nullable=False, server_default="#3B82F6"),
        sa.Column("group_name", sa.String(length=50), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "customer_tags",
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("tag_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("customer_id", "tag_id"),
    )

    # Enable pg_trgm extension
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # customers indexes
    op.create_index("idx_customers_tenant", "customers", ["tenant_id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_customers_owner", "customers", ["owner_id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_customers_grade", "customers", ["grade_id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_customers_source", "customers", ["source"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_customers_last_follow", "customers", ["last_follow_at"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.execute("CREATE INDEX idx_customers_name_trgm ON customers USING GIN (name gin_trgm_ops) WHERE deleted_at IS NULL")

    # contacts indexes
    op.create_index("idx_contacts_customer", "contacts", ["customer_id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_contacts_email", "contacts", ["email"], postgresql_where=sa.text("deleted_at IS NULL"))

    # tags unique index (expression-based for COALESCE)
    op.execute("CREATE UNIQUE INDEX idx_tags_tenant_name ON tags (tenant_id, name, COALESCE(group_name, '')) WHERE deleted_at IS NULL")

    # customer_grades index
    op.create_index("idx_grades_tenant", "customer_grades", ["tenant_id"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index("idx_grades_tenant", table_name="customer_grades")
    op.execute("DROP INDEX IF EXISTS idx_tags_tenant_name")
    op.drop_index("idx_contacts_email", table_name="contacts")
    op.drop_index("idx_contacts_customer", table_name="contacts")
    op.execute("DROP INDEX IF EXISTS idx_customers_name_trgm")
    op.drop_index("idx_customers_last_follow", table_name="customers")
    op.drop_index("idx_customers_source", table_name="customers")
    op.drop_index("idx_customers_grade", table_name="customers")
    op.drop_index("idx_customers_owner", table_name="customers")
    op.drop_index("idx_customers_tenant", table_name="customers")

    # Drop tables in reverse order
    op.drop_table("customer_tags")
    op.drop_table("contacts")
    op.drop_table("customers")
    op.drop_table("tags")
    op.drop_table("customer_grades")
