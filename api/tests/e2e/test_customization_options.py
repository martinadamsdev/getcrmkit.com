from httpx import AsyncClient


class TestCustomizationOptionCRUD:
    async def test_create_option(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post(
            "/api/v1/customization-options",
            json={
                "name": "Logo Printing",
                "description": "Custom logo on product",
                "extra_cost": "5.00",
                "extra_currency": "CNY",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Logo Printing"
        assert data["extra_cost"] == "5.00"  # AC-0.6.4: extra_cost works
        assert data["extra_currency"] == "CNY"

    async def test_create_option_empty_name(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post(
            "/api/v1/customization-options",
            json={"name": ""},
        )
        assert resp.status_code == 422
        assert resp.json()["detail"]["code"] == "CUSTOMIZATION_OPTION_NAME_REQUIRED"

    async def test_list_options(self, authenticated_client: AsyncClient) -> None:
        await authenticated_client.post("/api/v1/customization-options", json={"name": "Option A"})
        await authenticated_client.post("/api/v1/customization-options", json={"name": "Option B"})
        resp = await authenticated_client.get("/api/v1/customization-options")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_update_option(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post(
            "/api/v1/customization-options",
            json={"name": "Old Option", "extra_cost": "3.00"},
        )
        option_id = create_resp.json()["id"]
        resp = await authenticated_client.put(
            f"/api/v1/customization-options/{option_id}",
            json={"name": "Updated Option", "extra_cost": "10.00"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Option"
        assert resp.json()["extra_cost"] == "10.00"

    async def test_delete_option(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/customization-options", json={"name": "ToDelete"})
        option_id = create_resp.json()["id"]
        resp = await authenticated_client.delete(f"/api/v1/customization-options/{option_id}")
        assert resp.status_code == 204

    async def test_unauthenticated(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/customization-options")
        assert resp.status_code == 401
