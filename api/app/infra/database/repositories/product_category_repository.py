from __future__ import annotations

import uuid

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entities import ProductCategory
from app.domain.product.repository import AbstractProductCategoryRepository
from app.infra.database.models.product import ProductCategoryModel, ProductModel


class ProductCategoryRepository(AbstractProductCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, category: ProductCategory) -> ProductCategory:
        model = self._to_model(category)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> ProductCategory | None:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
            ProductCategoryModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, tenant_id: uuid.UUID) -> list[ProductCategory]:
        stmt = (
            select(ProductCategoryModel)
            .where(ProductCategoryModel.tenant_id == tenant_id)
            .order_by(ProductCategoryModel.level, ProductCategoryModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def get_children(self, tenant_id: uuid.UUID, parent_id: uuid.UUID) -> list[ProductCategory]:
        stmt = (
            select(ProductCategoryModel)
            .where(
                ProductCategoryModel.tenant_id == tenant_id,
                ProductCategoryModel.parent_id == parent_id,
            )
            .order_by(ProductCategoryModel.position)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars()]

    async def get_tree(self, tenant_id: uuid.UUID) -> list[ProductCategory]:
        # Return all categories ordered for tree construction (level + position)
        return await self.get_all(tenant_id)

    async def update(self, category: ProductCategory) -> ProductCategory:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category.id,
            ProductCategoryModel.tenant_id == category.tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        model.name = category.name
        model.parent_id = category.parent_id
        model.level = category.level
        model.position = category.position
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> None:
        stmt = select(ProductCategoryModel).where(
            ProductCategoryModel.id == category_id,
            ProductCategoryModel.tenant_id == tenant_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one()
        await self._session.delete(model)
        await self._session.flush()

    async def has_products(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> bool:
        stmt = select(
            exists().where(
                ProductModel.category_id == category_id,
                ProductModel.tenant_id == tenant_id,
                ProductModel.deleted_at.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return bool(result.scalar())

    async def has_children(self, tenant_id: uuid.UUID, category_id: uuid.UUID) -> bool:
        stmt = select(
            exists().where(
                ProductCategoryModel.parent_id == category_id,
                ProductCategoryModel.tenant_id == tenant_id,
            )
        )
        result = await self._session.execute(stmt)
        return bool(result.scalar())

    @staticmethod
    def _to_model(category: ProductCategory) -> ProductCategoryModel:
        return ProductCategoryModel(
            id=category.id,
            tenant_id=category.tenant_id,
            name=category.name,
            parent_id=category.parent_id,
            level=category.level,
            position=category.position,
            created_at=category.created_at,
        )

    @staticmethod
    def _to_entity(model: ProductCategoryModel) -> ProductCategory:
        return ProductCategory(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            parent_id=model.parent_id,
            level=model.level,
            position=model.position,
            created_at=model.created_at,
        )
