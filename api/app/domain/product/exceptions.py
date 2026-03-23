from app.domain.shared.exceptions import DomainError


class ProductNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Product name is required", code="PRODUCT_NAME_REQUIRED")


class ProductNotFoundError(DomainError):
    def __init__(self, product_id: str) -> None:
        super().__init__(message=f"Product not found: {product_id}", code="PRODUCT_NOT_FOUND")


class VariantNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Variant name is required", code="VARIANT_NAME_REQUIRED")


class VariantNotFoundError(DomainError):
    def __init__(self, variant_id: str) -> None:
        super().__init__(message=f"Product variant not found: {variant_id}", code="VARIANT_NOT_FOUND")


class CategoryNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Category name is required", code="CATEGORY_NAME_REQUIRED")


class CategoryNotFoundError(DomainError):
    def __init__(self, category_id: str) -> None:
        super().__init__(message=f"Product category not found: {category_id}", code="CATEGORY_NOT_FOUND")


class InvalidCategoryLevelError(DomainError):
    def __init__(self, level: int) -> None:
        super().__init__(message=f"Invalid category level: {level}, must be 1/2/3", code="INVALID_CATEGORY_LEVEL")


class MaxCategoryDepthError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Category depth cannot exceed 3 levels",
            code="MAX_CATEGORY_DEPTH",
        )


class CategoryHasChildrenError(DomainError):
    def __init__(self, category_id: str) -> None:
        super().__init__(
            message=f"Cannot delete category with children: {category_id}",
            code="CATEGORY_HAS_CHILDREN",
        )


class CategoryInUseError(DomainError):
    def __init__(self, category_id: str) -> None:
        super().__init__(
            message=f"Category is in use by products: {category_id}",
            code="CATEGORY_IN_USE",
        )


class PricingTierNotFoundError(DomainError):
    def __init__(self, tier_id: str) -> None:
        super().__init__(message=f"Pricing tier not found: {tier_id}", code="PRICING_TIER_NOT_FOUND")


class InvalidQuantityRangeError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(message=f"Invalid quantity range: {detail}", code="INVALID_QUANTITY_RANGE")


class InvalidMultiplierError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Multiplier must be positive", code="INVALID_MULTIPLIER")


class CustomizationOptionNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Customization option name is required",
            code="CUSTOMIZATION_OPTION_NAME_REQUIRED",
        )


class CustomizationOptionNotFoundError(DomainError):
    def __init__(self, option_id: str) -> None:
        super().__init__(
            message=f"Customization option not found: {option_id}",
            code="CUSTOMIZATION_OPTION_NOT_FOUND",
        )


class OptionNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Customization option name is required", code="OPTION_NAME_REQUIRED")


class InvalidExtraCostError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Extra cost cannot be negative", code="INVALID_EXTRA_COST")
