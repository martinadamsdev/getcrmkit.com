from app.domain.product.exceptions import (
    CategoryHasChildrenError,
    CategoryInUseError,
    CategoryNameRequiredError,
    CategoryNotFoundError,
    CustomizationOptionNameRequiredError,
    CustomizationOptionNotFoundError,
    InvalidCategoryLevelError,
    InvalidExtraCostError,
    InvalidMultiplierError,
    InvalidQuantityRangeError,
    MaxCategoryDepthError,
    OptionNameRequiredError,
    PricingTierNotFoundError,
    ProductNameRequiredError,
    ProductNotFoundError,
    VariantNameRequiredError,
    VariantNotFoundError,
)


class TestProductExceptions:
    def test_product_name_required(self):
        e = ProductNameRequiredError()
        assert e.code == "PRODUCT_NAME_REQUIRED"

    def test_product_not_found(self):
        e = ProductNotFoundError("abc-123")
        assert e.code == "PRODUCT_NOT_FOUND"
        assert "abc-123" in e.message

    def test_variant_name_required(self):
        e = VariantNameRequiredError()
        assert e.code == "VARIANT_NAME_REQUIRED"

    def test_variant_not_found(self):
        e = VariantNotFoundError("v-123")
        assert e.code == "VARIANT_NOT_FOUND"
        assert "v-123" in e.message

    def test_category_name_required(self):
        e = CategoryNameRequiredError()
        assert e.code == "CATEGORY_NAME_REQUIRED"

    def test_category_not_found(self):
        e = CategoryNotFoundError("c-123")
        assert e.code == "CATEGORY_NOT_FOUND"
        assert "c-123" in e.message

    def test_invalid_category_level(self):
        e = InvalidCategoryLevelError(5)
        assert e.code == "INVALID_CATEGORY_LEVEL"
        assert "5" in e.message

    def test_max_category_depth(self):
        e = MaxCategoryDepthError()
        assert e.code == "MAX_CATEGORY_DEPTH"

    def test_category_has_children(self):
        e = CategoryHasChildrenError("c-456")
        assert e.code == "CATEGORY_HAS_CHILDREN"
        assert "c-456" in e.message

    def test_category_in_use(self):
        e = CategoryInUseError("c-789")
        assert e.code == "CATEGORY_IN_USE"
        assert "c-789" in e.message

    def test_pricing_tier_not_found(self):
        e = PricingTierNotFoundError("t-123")
        assert e.code == "PRICING_TIER_NOT_FOUND"

    def test_invalid_quantity_range(self):
        e = InvalidQuantityRangeError("min > max")
        assert e.code == "INVALID_QUANTITY_RANGE"
        assert "min > max" in e.message

    def test_invalid_multiplier(self):
        e = InvalidMultiplierError()
        assert e.code == "INVALID_MULTIPLIER"

    def test_customization_option_name_required(self):
        e = CustomizationOptionNameRequiredError()
        assert e.code == "CUSTOMIZATION_OPTION_NAME_REQUIRED"

    def test_customization_option_not_found(self):
        e = CustomizationOptionNotFoundError("o-123")
        assert e.code == "CUSTOMIZATION_OPTION_NOT_FOUND"

    def test_option_name_required(self):
        e = OptionNameRequiredError()
        assert e.code == "OPTION_NAME_REQUIRED"

    def test_invalid_extra_cost(self):
        e = InvalidExtraCostError()
        assert e.code == "INVALID_EXTRA_COST"
