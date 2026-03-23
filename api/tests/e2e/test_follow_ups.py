import uuid

from httpx import AsyncClient


class TestFollowUps:
    async def _create_customer(self, client: AsyncClient) -> str:
        response = await client.post("/api/v1/customers", json={"name": "Follow-up Test Customer"})
        assert response.status_code == 201
        return response.json()["id"]

    async def test_create_follow_up(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        response = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "email",
                "content": "Sent initial quotation",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Sent initial quotation"
        assert data["method"] == "email"
        assert data["customer_id"] == customer_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_follow_up_updates_customer_last_follow_at(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)

        # Verify last_follow_at is initially None
        customer = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert customer.json()["last_follow_at"] is None

        # Create follow-up
        await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "wechat",
                "content": "Discussed product details",
            },
        )

        # Verify last_follow_at is updated
        customer = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert customer.json()["last_follow_at"] is not None

    async def test_create_follow_up_customer_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": fake_id,
                "method": "email",
                "content": "Hello",
            },
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

    async def test_create_follow_up_empty_content(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        response = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "email",
                "content": "   ",
            },
        )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "FOLLOW_UP_CONTENT_REQUIRED"

    async def test_create_follow_up_with_all_fields(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        response = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "alibaba",
                "content": "Alibaba message sent",
                "stage": "contacted",
                "customer_response": "Interested in product A",
                "next_follow_at": "2026-04-01T10:00:00Z",
                "tags": ["urgent", "sample"],
                "attachment_urls": ["https://s3.example.com/quotation.pdf"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["method"] == "alibaba"
        assert data["stage"] == "contacted"
        assert data["customer_response"] == "Interested in product A"
        assert data["tags"] == ["urgent", "sample"]
        assert data["attachment_urls"] == ["https://s3.example.com/quotation.pdf"]

    async def test_list_follow_ups(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        for i in range(3):
            await authenticated_client.post(
                "/api/v1/follow-ups",
                json={
                    "customer_id": customer_id,
                    "method": "email",
                    "content": f"Follow-up {i}",
                },
            )

        response = await authenticated_client.get("/api/v1/follow-ups")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    async def test_list_follow_ups_with_tags_filter(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)

        # Create follow-ups with different tags
        await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "email",
                "content": "Tagged follow-up",
                "tags": ["urgent"],
            },
        )
        await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "phone",
                "content": "Untagged follow-up",
            },
        )

        response = await authenticated_client.get("/api/v1/follow-ups?tags=urgent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["tags"] == ["urgent"]

    async def test_get_follow_up_by_id(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        create = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "meeting",
                "content": "Face-to-face meeting at exhibition",
            },
        )
        follow_up_id = create.json()["id"]

        response = await authenticated_client.get(f"/api/v1/follow-ups/{follow_up_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == follow_up_id
        assert data["content"] == "Face-to-face meeting at exhibition"

    async def test_get_follow_up_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.get(f"/api/v1/follow-ups/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "FOLLOW_UP_NOT_FOUND"

    async def test_update_follow_up(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        create = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "email",
                "content": "Original content",
            },
        )
        follow_up_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/follow-ups/{follow_up_id}",
            json={"content": "Updated content", "tags": ["important"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated content"
        assert data["tags"] == ["important"]

    async def test_update_follow_up_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/follow-ups/{fake_id}",
            json={"content": "Ghost"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "FOLLOW_UP_NOT_FOUND"

    async def test_delete_follow_up(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        create = await authenticated_client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": "email",
                "content": "To be deleted",
            },
        )
        follow_up_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/follow-ups/{follow_up_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = await authenticated_client.get(f"/api/v1/follow-ups/{follow_up_id}")
        assert response.status_code == 404

    async def test_delete_follow_up_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/follow-ups/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "FOLLOW_UP_NOT_FOUND"

    async def test_customer_timeline(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)

        # Create multiple follow-ups
        for i in range(3):
            await authenticated_client.post(
                "/api/v1/follow-ups",
                json={
                    "customer_id": customer_id,
                    "method": "email",
                    "content": f"Timeline entry {i}",
                },
            )

        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}/timeline")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

        # Verify DESC order (latest first)
        dates = [item["created_at"] for item in data["items"]]
        assert dates == sorted(dates, reverse=True)

    async def test_customer_timeline_empty(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)

        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}/timeline")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
