import uuid

from httpx import AsyncClient


class TestSavedViews:
    async def test_crud_lifecycle(self, authenticated_client: AsyncClient):
        # Create
        response = await authenticated_client.post(
            "/api/v1/saved-views",
            json={
                "name": "My VIP View",
                "entity_type": "customer",
                "filter_config": {"source": "alibaba"},
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "My VIP View"
        assert data["entity_type"] == "customer"
        assert data["filter_config"] == {"source": "alibaba"}
        assert "id" in data
        view_id = data["id"]

        # List
        response = await authenticated_client.get("/api/v1/saved-views?entity_type=customer")
        assert response.status_code == 200
        views = response.json()
        assert any(v["id"] == view_id for v in views)

        # Update
        response = await authenticated_client.put(
            f"/api/v1/saved-views/{view_id}",
            json={"name": "Updated View", "filter_config": {"source": "exhibition"}},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated View"
        assert data["filter_config"] == {"source": "exhibition"}

        # Delete
        response = await authenticated_client.delete(f"/api/v1/saved-views/{view_id}")
        assert response.status_code == 204

    async def test_create_duplicate_name(self, authenticated_client: AsyncClient):
        await authenticated_client.post(
            "/api/v1/saved-views",
            json={"name": "Duplicate", "filter_config": {"source": "a"}},
        )
        response = await authenticated_client.post(
            "/api/v1/saved-views",
            json={"name": "Duplicate", "filter_config": {"source": "b"}},
        )
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "DUPLICATE_VIEW_NAME"

    async def test_update_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/saved-views/{fake_id}",
            json={"name": "Ghost"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "SAVED_VIEW_NOT_FOUND"

    async def test_delete_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/saved-views/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "SAVED_VIEW_NOT_FOUND"

    async def test_unauthenticated(self, client: AsyncClient):
        response = await client.get("/api/v1/saved-views")
        assert response.status_code == 401
