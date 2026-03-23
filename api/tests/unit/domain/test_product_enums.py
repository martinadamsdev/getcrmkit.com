def test_product_enums_module_importable():
    """Product domain enums module exists and is importable."""
    import app.domain.product.enums  # noqa: F401
