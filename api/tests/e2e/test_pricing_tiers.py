from httpx import AsyncClient


class TestPricingTierCRUD:
    async def test_create_pricing_tier(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={
                "name": "Small Order",
                "min_qty": 1,
                "max_qty": 99,
                "multiplier": "1.5000",
                "position": 0,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Small Order"
        assert data["min_qty"] == 1
        assert data["max_qty"] == 99
        assert data["multiplier"] == "1.5000"

    async def test_list_pricing_tiers(self, authenticated_client: AsyncClient) -> None:
        await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Tier A", "min_qty": 1, "multiplier": "1.2", "position": 0},
        )
        await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Tier B", "min_qty": 100, "multiplier": "1.0", "position": 1},
        )
        resp = await authenticated_client.get("/api/v1/pricing-tiers")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_update_pricing_tier(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Old", "min_qty": 1, "multiplier": "1.5"},
        )
        tier_id = create_resp.json()["id"]
        resp = await authenticated_client.put(
            f"/api/v1/pricing-tiers/{tier_id}",
            json={"name": "Updated", "multiplier": "2.0"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"
        assert resp.json()["multiplier"] == "2.0"

    async def test_delete_pricing_tier(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "ToDelete", "min_qty": 1, "multiplier": "1.0"},
        )
        tier_id = create_resp.json()["id"]
        resp = await authenticated_client.delete(f"/api/v1/pricing-tiers/{tier_id}")
        assert resp.status_code == 204

    async def test_get_multiplier(self, authenticated_client: AsyncClient) -> None:
        """AC-0.6.2: GET /pricing-tiers/multiplier?qty=250 returns correct multiplier."""
        # Create tiers: 1-99 -> 1.5, 100-499 -> 1.2, 500+ -> 1.0
        await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Small", "min_qty": 1, "max_qty": 99, "multiplier": "1.5000", "position": 0},
        )
        await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Medium", "min_qty": 100, "max_qty": 499, "multiplier": "1.2000", "position": 1},
        )
        await authenticated_client.post(
            "/api/v1/pricing-tiers",
            json={"name": "Large", "min_qty": 500, "multiplier": "1.0000", "position": 2},
        )

        resp = await authenticated_client.get("/api/v1/pricing-tiers/multiplier", params={"qty": 250})
        assert resp.status_code == 200
        data = resp.json()
        assert data["qty"] == 250
        assert data["multiplier"] == "1.2000"

    async def test_get_multiplier_no_match_returns_default(self, authenticated_client: AsyncClient) -> None:
        """No matching tier returns 1.0000."""
        resp = await authenticated_client.get("/api/v1/pricing-tiers/multiplier", params={"qty": 999})
        assert resp.status_code == 200
        assert resp.json()["multiplier"] == "1.0000"

    async def test_unauthenticated(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/pricing-tiers")
        assert resp.status_code == 401
