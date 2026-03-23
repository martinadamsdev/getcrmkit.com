from httpx import AsyncClient


class TestProductCategoryCRUD:
    async def test_create_category(self, authenticated_client: AsyncClient) -> None:
        resp = await authenticated_client.post(
            "/api/v1/product-categories",
            json={"name": "Electronics", "position": 0},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Electronics"
        assert data["level"] == 1
        assert data["parent_id"] is None

    async def test_list_categories(self, authenticated_client: AsyncClient) -> None:
        await authenticated_client.post("/api/v1/product-categories", json={"name": "Cat A"})
        await authenticated_client.post("/api/v1/product-categories", json={"name": "Cat B"})
        resp = await authenticated_client.get("/api/v1/product-categories")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_update_category(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/product-categories", json={"name": "OldName"})
        cat_id = create_resp.json()["id"]
        resp = await authenticated_client.put(
            f"/api/v1/product-categories/{cat_id}",
            json={"name": "NewName"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "NewName"

    async def test_delete_category(self, authenticated_client: AsyncClient) -> None:
        create_resp = await authenticated_client.post("/api/v1/product-categories", json={"name": "ToDelete"})
        cat_id = create_resp.json()["id"]
        resp = await authenticated_client.delete(f"/api/v1/product-categories/{cat_id}")
        assert resp.status_code == 204

    async def test_three_level_tree(self, authenticated_client: AsyncClient) -> None:
        """AC-0.6.5: 3 levels work."""
        # Level 1
        l1 = await authenticated_client.post("/api/v1/product-categories", json={"name": "Level 1"})
        assert l1.status_code == 201
        l1_id = l1.json()["id"]
        assert l1.json()["level"] == 1

        # Level 2
        l2 = await authenticated_client.post("/api/v1/product-categories", json={"name": "Level 2", "parent_id": l1_id})
        assert l2.status_code == 201
        l2_id = l2.json()["id"]
        assert l2.json()["level"] == 2

        # Level 3
        l3 = await authenticated_client.post("/api/v1/product-categories", json={"name": "Level 3", "parent_id": l2_id})
        assert l3.status_code == 201
        assert l3.json()["level"] == 3

    async def test_fourth_level_rejected(self, authenticated_client: AsyncClient) -> None:
        """AC-0.6.5: 4th level -> 422."""
        l1 = await authenticated_client.post("/api/v1/product-categories", json={"name": "L1"})
        l1_id = l1.json()["id"]
        l2 = await authenticated_client.post("/api/v1/product-categories", json={"name": "L2", "parent_id": l1_id})
        l2_id = l2.json()["id"]
        l3 = await authenticated_client.post("/api/v1/product-categories", json={"name": "L3", "parent_id": l2_id})
        l3_id = l3.json()["id"]

        # Level 4 should fail
        resp = await authenticated_client.post("/api/v1/product-categories", json={"name": "L4", "parent_id": l3_id})
        assert resp.status_code == 422
        assert resp.json()["detail"]["code"] == "MAX_CATEGORY_DEPTH"

    async def test_delete_category_has_children_409(self, authenticated_client: AsyncClient) -> None:
        parent = await authenticated_client.post("/api/v1/product-categories", json={"name": "Parent"})
        parent_id = parent.json()["id"]
        await authenticated_client.post("/api/v1/product-categories", json={"name": "Child", "parent_id": parent_id})
        resp = await authenticated_client.delete(f"/api/v1/product-categories/{parent_id}")
        assert resp.status_code == 409
        assert resp.json()["detail"]["code"] == "CATEGORY_HAS_CHILDREN"

    async def test_delete_category_has_products_409(self, authenticated_client: AsyncClient) -> None:
        cat = await authenticated_client.post("/api/v1/product-categories", json={"name": "InUse"})
        cat_id = cat.json()["id"]
        await authenticated_client.post("/api/v1/products", json={"name": "Product In Cat", "category_id": cat_id})
        resp = await authenticated_client.delete(f"/api/v1/product-categories/{cat_id}")
        assert resp.status_code == 409
        assert resp.json()["detail"]["code"] == "CATEGORY_IN_USE"

    async def test_unauthenticated(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/product-categories")
        assert resp.status_code == 401
