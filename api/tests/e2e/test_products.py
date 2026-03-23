import uuid

from httpx import AsyncClient


class TestProductCRUD:
    async def test_create_product(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post(
            "/api/v1/products",
            json={
                "name": "Widget Pro",
                "sku": "WP-001",
                "cost_price": "45.50",
                "cost_currency": "CNY",
                "selling_price": "12.99",
                "selling_currency": "USD",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Widget Pro"
        assert data["sku"] == "WP-001"
        assert data["image_url"] is None  # AC-0.6.1: image_url field exists

    async def test_create_product_empty_name(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post("/api/v1/products", json={"name": ""})
        assert resp.status_code == 422

    async def test_list_products(self, authenticated_client: AsyncClient) -> None:
        await authenticated_client.post("/api/v1/products", json={"name": "Widget A"})
        await authenticated_client.post("/api/v1/products", json={"name": "Widget B"})
        resp = await authenticated_client.get("/api/v1/products")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2

    async def test_list_products_with_filter(self, authenticated_client: AsyncClient) -> None:
        await authenticated_client.post("/api/v1/products", json={"name": "Alpha Widget"})
        await authenticated_client.post("/api/v1/products", json={"name": "Beta Gadget"})
        resp = await authenticated_client.get("/api/v1/products", params={"keyword": "Alpha"})
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    async def test_get_product(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/products", json={"name": "Widget"})
        product_id = create_resp.json()["id"]
        resp = await authenticated_client.get(f"/api/v1/products/{product_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Widget"

    async def test_get_product_not_found(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.get(f"/api/v1/products/{uuid.uuid7()}")
        assert resp.status_code == 404
        assert resp.json()["detail"]["code"] == "PRODUCT_NOT_FOUND"

    async def test_update_product(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/products", json={"name": "Widget"})
        product_id = create_resp.json()["id"]
        resp = await authenticated_client.put(
            f"/api/v1/products/{product_id}",
            json={"name": "Widget Pro"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Widget Pro"

    async def test_delete_product(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/products", json={"name": "Widget"})
        product_id = create_resp.json()["id"]
        resp = await authenticated_client.delete(f"/api/v1/products/{product_id}")
        assert resp.status_code == 204

        # Verify soft delete
        resp = await authenticated_client.get(f"/api/v1/products/{product_id}")
        assert resp.status_code == 404

    async def test_unauthenticated(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/products")
        assert resp.status_code == 401
