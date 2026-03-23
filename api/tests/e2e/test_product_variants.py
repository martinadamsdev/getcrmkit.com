import uuid

from httpx import AsyncClient


class TestProductVariantCRUD:
    async def _create_product(self, client: AsyncClient) -> str:
        resp = await client.post("/api/v1/products", json={"name": "Variant Host Product"})
        assert resp.status_code == 201
        return resp.json()["id"]

    async def test_create_variant(self, authenticated_client: AsyncClient) -> None:
        product_id = await self._create_product(authenticated_client)
        resp = await authenticated_client.post(
            f"/api/v1/products/{product_id}/variants",
            json={
                "variant_name": "Red / L",
                "sku": "VAR-001",
                "color_code": "#FF0000",
                "cost_price": "25.50",
                "cost_currency": "USD",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["variant_name"] == "Red / L"
        assert data["color_code"] == "#FF0000"  # AC-0.6.3: color_code present
        assert data["sku"] == "VAR-001"  # AC-0.6.3: independent SKU
        assert data["cost_price"] == "25.50"  # AC-0.6.3: independent cost_price

    async def test_list_variants(self, authenticated_client: AsyncClient) -> None:
        product_id = await self._create_product(authenticated_client)
        await authenticated_client.post(
            f"/api/v1/products/{product_id}/variants",
            json={"variant_name": "Red / L"},
        )
        await authenticated_client.post(
            f"/api/v1/products/{product_id}/variants",
            json={"variant_name": "Blue / M"},
        )
        resp = await authenticated_client.get(f"/api/v1/products/{product_id}/variants")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_update_variant(self, authenticated_client: AsyncClient) -> None:
        product_id = await self._create_product(authenticated_client)
        create_resp = await authenticated_client.post(
            f"/api/v1/products/{product_id}/variants",
            json={"variant_name": "Red / L"},
        )
        variant_id = create_resp.json()["id"]
        resp = await authenticated_client.put(
            f"/api/v1/products/{product_id}/variants/{variant_id}",
            json={"variant_name": "Red / XL"},
        )
        assert resp.status_code == 200
        assert resp.json()["variant_name"] == "Red / XL"

    async def test_delete_variant(self, authenticated_client: AsyncClient) -> None:
        product_id = await self._create_product(authenticated_client)
        create_resp = await authenticated_client.post(
            f"/api/v1/products/{product_id}/variants",
            json={"variant_name": "Red / L"},
        )
        variant_id = create_resp.json()["id"]
        resp = await authenticated_client.delete(f"/api/v1/products/{product_id}/variants/{variant_id}")
        assert resp.status_code == 204

    async def test_create_variant_product_not_found(self, authenticated_client: AsyncClient) -> None:
        fake_id = str(uuid.uuid7())
        resp = await authenticated_client.post(
            f"/api/v1/products/{fake_id}/variants",
            json={"variant_name": "Ghost Variant"},
        )
        assert resp.status_code == 404
        assert resp.json()["detail"]["code"] == "PRODUCT_NOT_FOUND"

    async def test_unauthenticated(self, client: AsyncClient) -> None:
        fake_id = str(uuid.uuid7())
        resp = await client.get(f"/api/v1/products/{fake_id}/variants")
        assert resp.status_code == 401
