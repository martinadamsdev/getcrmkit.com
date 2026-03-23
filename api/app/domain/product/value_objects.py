# NOTE: Money already exists in domain/shared/value_objects.py — do NOT redefine here.
# Import Money from shared: `from app.domain.shared.value_objects import Money`
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class ProductFilter:
    keyword: str | None = None  # pg_trgm 模糊搜索（产品名）
    category_id: uuid.UUID | None = None  # 精确（含子分类递归）
    is_active: bool | None = None  # 精确
    min_cost: Decimal | None = None  # 成本价范围
    max_cost: Decimal | None = None
    min_selling: Decimal | None = None  # 售价范围
    max_selling: Decimal | None = None
    created_at_from: datetime | None = None  # 范围
    created_at_to: datetime | None = None  # 范围
    sort_by: Literal["created_at", "name", "sku", "cost_price", "selling_price"] = "created_at"
    sort: Literal["asc", "desc"] = "desc"
