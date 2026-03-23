from httpx import AsyncClient


class TestDuplicateCheck:
    async def test_check_duplicate_name_exact(self, authenticated_client: AsyncClient):
        await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Acme Corp"},
        )
        # Add a contact with email for domain matching
        customers = await authenticated_client.get("/api/v1/customers")
        customer_id = customers.json()["items"][0]["id"]
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "John", "email": "john@acme.com"},
        )

        response = await authenticated_client.post(
            "/api/v1/customers/check-duplicate",
            json={"name": "Acme Corp"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["duplicates"]) >= 1
        match_types = [d["match_type"] for d in data["duplicates"]]
        assert "name_exact" in match_types

    async def test_check_duplicate_email_domain(self, authenticated_client: AsyncClient):
        customer = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Acme Corp"},
        )
        customer_id = customer.json()["id"]
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "John", "email": "john@acme.com"},
        )

        response = await authenticated_client.post(
            "/api/v1/customers/check-duplicate",
            json={"name": "Other Corp", "email": "x@acme.com"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["duplicates"]) >= 1
        match_types = [d["match_type"] for d in data["duplicates"]]
        assert "email_domain" in match_types

    async def test_check_duplicate_no_match(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/customers/check-duplicate",
            json={"name": "Nobody Corp"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["duplicates"] == []

    async def test_check_duplicate_unauthenticated(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/customers/check-duplicate",
            json={"name": "Test"},
        )
        assert response.status_code == 401
