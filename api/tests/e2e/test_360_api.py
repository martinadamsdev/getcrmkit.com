import uuid

from httpx import AsyncClient


class TestCustomer360:
    async def test_get_360_view(self, authenticated_client: AsyncClient):
        # Create grade
        grade = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "VIP", "color": "#FF0000"},
        )
        grade_id = grade.json()["id"]

        # Create tag
        tag = await authenticated_client.post(
            "/api/v1/tags",
            json={"name": "priority"},
        )
        tag_id = tag.json()["id"]

        # Create customer with grade
        customer = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "360 Corp", "grade_id": grade_id, "country": "US"},
        )
        customer_id = customer.json()["id"]

        # Tag customer
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/tags",
            json={"tag_id": tag_id},
        )

        # Add contacts
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Alice", "email": "alice@360.com"},
        )
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Bob", "email": "bob@360.com"},
        )

        # Get 360 view
        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}/360")
        assert response.status_code == 200
        data = response.json()

        assert data["customer"]["name"] == "360 Corp"
        assert data["customer"]["grade_id"] == grade_id
        assert data["grade"]["name"] == "VIP"
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "priority"
        assert len(data["contacts"]) == 2
        contact_names = [c["name"] for c in data["contacts"]]
        assert "Alice" in contact_names
        assert "Bob" in contact_names
        assert data["follow_ups"] == []
        assert data["quotations"] == []
        assert data["orders"] == []
        assert data["stats"]["contact_count"] == 2
        assert data["stats"]["follow_up_count"] == 0
        assert data["stats"]["quotation_count"] == 0
        assert data["stats"]["order_count"] == 0

    async def test_get_360_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.get(f"/api/v1/customers/{fake_id}/360")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

    async def test_get_360_unauthenticated(self, client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await client.get(f"/api/v1/customers/{fake_id}/360")
        assert response.status_code == 401
