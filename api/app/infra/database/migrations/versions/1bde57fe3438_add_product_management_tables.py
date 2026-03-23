"""add product management tables

Revision ID: 1bde57fe3438
Revises: d8cc1e21eae6
Create Date: 2026-03-24 00:08:06.335579

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1bde57fe3438"
down_revision: str | Sequence[str] | None = "d8cc1e21eae6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- product_categories ---
    op.create_table(
        "product_categories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("parent_id", sa.Uuid(), nullable=True),
        sa.Column("level", sa.SmallInteger(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["product_categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_product_categories_tenant", "product_categories", ["tenant_id"])
    op.create_index("idx_product_categories_parent", "product_categories", ["parent_id"])

    # --- products ---
    op.create_table(
        "products",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=True),
        sa.Column("category_id", sa.Uuid(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("material", sa.String(length=100), nullable=True),
        sa.Column("dimensions", sa.String(length=100), nullable=True),
        sa.Column("weight", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("color", sa.String(length=50), nullable=True),
        sa.Column("packing", sa.String(length=200), nullable=True),
        sa.Column("cost_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("cost_currency", sa.String(length=3), nullable=False),
        sa.Column("selling_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("selling_currency", sa.String(length=3), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("custom_fields", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=True),
        sa.Column("updated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["product_categories.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_products_tenant",
        "products",
        ["tenant_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_products_category",
        "products",
        ["category_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_products_name_trgm",
        "products",
        ["name"],
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "idx_products_tenant_sku",
        "products",
        ["tenant_id", "sku"],
        unique=True,
        postgresql_where=sa.text("sku IS NOT NULL AND deleted_at IS NULL"),
    )

    # --- product_variants ---
    op.create_table(
        "product_variants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.Column("variant_name", sa.String(length=200), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=True),
        sa.Column("material", sa.String(length=100), nullable=True),
        sa.Column("color", sa.String(length=50), nullable=True),
        sa.Column("color_code", sa.String(length=7), nullable=True),
        sa.Column("size", sa.String(length=50), nullable=True),
        sa.Column("cost_price", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("cost_currency", sa.String(length=3), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_product_variants_product", "product_variants", ["product_id"])
    op.create_index("idx_product_variants_tenant", "product_variants", ["tenant_id"])
    op.create_index(
        "idx_product_variants_tenant_sku",
        "product_variants",
        ["tenant_id", "sku"],
        unique=True,
        postgresql_where=sa.text("sku IS NOT NULL"),
    )

    # --- pricing_tiers ---
    op.create_table(
        "pricing_tiers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=True),
        sa.Column("min_qty", sa.Integer(), nullable=False),
        sa.Column("max_qty", sa.Integer(), nullable=True),
        sa.Column("multiplier", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_pricing_tiers_tenant", "pricing_tiers", ["tenant_id"])

    # --- customization_options ---
    op.create_table(
        "customization_options",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("extra_cost", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("extra_currency", sa.String(length=3), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_customization_options_tenant", "customization_options", ["tenant_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("product_variants")
    op.drop_table("products")
    op.drop_table("product_categories")
    op.drop_table("pricing_tiers")
    op.drop_table("customization_options")
