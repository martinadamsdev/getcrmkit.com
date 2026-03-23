from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import Product
from app.domain.product.repository import AbstractProductRepository
from app.domain.product.value_objects import ProductFilter
from app.infra.database.models.product import ProductModel

SORT_COLUMNS: dict[str, object] = {
    "created_at": ProductModel.created_at,
    "name": ProductModel.name,
    "sku": ProductModel.sku,
    "cost_price": ProductModel.cost_price,
    "selling_price": ProductModel.selling_price,
}


class ProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, product: Product) -> Product:
        model = self._to_model(product)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> Product | None:
        stmt = select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.tenant_id == tenant_id,
            ProductModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_tenant(
        self,
        tenant_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        filters: ProductFilter | None = None,
    ) -> tuple[list[Product], int]:
        conditions = [
            ProductModel.tenant_id == tenant_id,
            ProductModel.deleted_at.is_(None),
        ]

        if filters is not None:
            if filters.keyword:
                conditions.append(ProductModel.name.op("%")(filters.keyword))
            if filters.category_id is not None:
                conditions.append(ProductModel.category_id == filters.category_id)
            if filters.is_active is not None:
                conditions.append(ProductModel.is_active == filters.is_active)
            if filters.min_cost is not None:
                conditions.append(ProductModel.cost_price >= filters.min_cost)
            if filters.max_cost is not None:
                conditions.append(ProductModel.cost_price <= filters.max_cost)
            if filters.min_selling is not None:
                conditions.append(ProductModel.selling_price >= filters.min_selling)
            if filters.max_selling is not None:
                conditions.append(ProductModel.selling_price <= filters.max_selling)
            if filters.created_at_from is not None:
                conditions.append(ProductModel.created_at >= filters.created_at_from)
            if filters.created_at_to is not None:
                conditions.append(ProductModel.created_at <= filters.created_at_to)

        count_stmt = select(func.count()).select_from(ProductModel).where(*conditions)
        total = (await self._session.execute(count_stmt)).scalar_one()

        # Sort
        sort_col = SORT_COLUMNS.get(filters.sort_by if filters else "created_at", ProductModel.created_at)
        sort = filters.sort if filters else "desc"
        order_clause = sort_col.asc() if sort == "asc" else sort_col.desc()  # type: ignore[attr-defined]

        stmt = (
            select(ProductModel)
            .where(*conditions)
            .order_by(order_clause)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_entity(m) for m in result.scalars()]
        return items, total

    async def update(self, product: Product) -> Product:
        stmt = select(ProductModel).where(
            ProductModel.id == product.id,
            ProductModel.tenant_id == product.tenant_id,
            ProductModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = product.name
        model.sku = product.sku
        model.category_id = product.category_id
        model.description = product.description
        model.image_url = product.image_url
        model.material = product.material
        model.dimensions = product.dimensions
        model.weight = product.weight
        model.color = product.color
        model.packing = product.packing
        model.cost_price = product.cost_price
        model.cost_currency = product.cost_currency
        model.selling_price = product.selling_price
        model.selling_currency = product.selling_currency
        model.is_active = product.is_active
        model.custom_fields = product.custom_fields
        model.updated_by = product.updated_by
        model.updated_at = product.updated_at
        await self._session.flush()
        return self._to_entity(model)

    async def soft_delete(self, tenant_id: uuid.UUID, product_id: uuid.UUID) -> None:
        stmt = select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.tenant_id == tenant_id,
            ProductModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.deleted_at = datetime.now(UTC)
        await self._session.flush()

    async def get_by_sku(self, tenant_id: uuid.UUID, sku: str) -> Product | None:
        stmt = select(ProductModel).where(
            ProductModel.tenant_id == tenant_id,
            ProductModel.sku == sku,
            ProductModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def count_by_tenant(self, tenant_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ProductModel)
            .where(
                ProductModel.tenant_id == tenant_id,
                ProductModel.deleted_at.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def get_by_category(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> list[Product]:
        stmt = select(ProductModel).where(
            ProductModel.tenant_id == tenant_id,
            ProductModel.category_id == category_id,
            ProductModel.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    @staticmethod
    def _to_model(product: Product) -> ProductModel:
        return ProductModel(
            id=product.id,
            tenant_id=product.tenant_id,
            name=product.name,
            sku=product.sku,
            category_id=product.category_id,
            description=product.description,
            image_url=product.image_url,
            material=product.material,
            dimensions=product.dimensions,
            weight=product.weight,
            color=product.color,
            packing=product.packing,
            cost_price=product.cost_price,
            cost_currency=product.cost_currency,
            selling_price=product.selling_price,
            selling_currency=product.selling_currency,
            is_active=product.is_active,
            custom_fields=product.custom_fields,
            created_by=product.created_by,
            updated_by=product.updated_by,
            created_at=product.created_at,
            updated_at=product.updated_at,
            deleted_at=product.deleted_at,
        )

    @staticmethod
    def _to_entity(model: ProductModel) -> Product:
        return Product(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            sku=model.sku,
            category_id=model.category_id,
            description=model.description,
            image_url=model.image_url,
            material=model.material,
            dimensions=model.dimensions,
            weight=model.weight,
            color=model.color,
            packing=model.packing,
            cost_price=model.cost_price,
            cost_currency=model.cost_currency,
            selling_price=model.selling_price,
            selling_currency=model.selling_currency,
            is_active=model.is_active,
            custom_fields=model.custom_fields,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
