import uuid

from httpx import AsyncClient

# ---------------------------------------------------------------------------
# Customer Grades
# ---------------------------------------------------------------------------


class TestCustomerGrades:
    async def test_list_grades_empty(self, authenticated_client: AsyncClient):
        response = await authenticated_client.get("/api/v1/customer-grades")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_grade(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "VIP", "label": "VIP Customer", "color": "#FF0000", "position": 1},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "VIP"
        assert data["label"] == "VIP Customer"
        assert data["color"] == "#FF0000"
        assert data["position"] == 1
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_update_grade(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "Silver", "color": "#C0C0C0"},
        )
        grade_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/customer-grades/{grade_id}",
            json={"name": "Gold", "color": "#FFD700"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Gold"
        assert data["color"] == "#FFD700"

    async def test_delete_grade_success(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "DeleteMe"},
        )
        grade_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/customer-grades/{grade_id}")
        assert response.status_code == 204

    async def test_delete_grade_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/customer-grades/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_GRADE_NOT_FOUND"

    async def test_update_grade_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/customer-grades/{fake_id}",
            json={"name": "Ghost"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_GRADE_NOT_FOUND"

    async def test_delete_grade_in_use(self, authenticated_client: AsyncClient):
        grade = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "InUse"},
        )
        grade_id = grade.json()["id"]

        await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Customer With Grade", "grade_id": grade_id},
        )

        response = await authenticated_client.delete(f"/api/v1/customer-grades/{grade_id}")
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "GRADE_IN_USE"


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------


class TestTags:
    async def test_create_tag(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/tags",
            json={"name": "hot lead", "color": "#FF4500"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "hot lead"
        assert data["color"] == "#FF4500"
        assert "id" in data

    async def test_list_tags(self, authenticated_client: AsyncClient):
        await authenticated_client.post("/api/v1/tags", json={"name": "important"})
        response = await authenticated_client.get("/api/v1/tags")
        assert response.status_code == 200
        names = [t["name"] for t in response.json()]
        assert "important" in names

    async def test_update_tag(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post("/api/v1/tags", json={"name": "old name"})
        tag_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/tags/{tag_id}",
            json={"name": "new name", "color": "#00FF00"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "new name"
        assert data["color"] == "#00FF00"

    async def test_delete_tag(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post("/api/v1/tags", json={"name": "to delete"})
        tag_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/tags/{tag_id}")
        assert response.status_code == 204

    async def test_create_duplicate_tag(self, authenticated_client: AsyncClient):
        await authenticated_client.post("/api/v1/tags", json={"name": "duplicate"})
        response = await authenticated_client.post("/api/v1/tags", json={"name": "duplicate"})
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "DUPLICATE_TAG"

    async def test_delete_tag_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/tags/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "TAG_NOT_FOUND"

    async def test_update_tag_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/tags/{fake_id}",
            json={"name": "ghost"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "TAG_NOT_FOUND"


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------


class TestCustomers:
    async def test_create_customer(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/customers",
            json={
                "name": "Acme Corp",
                "country": "CN",
                "industry": "Manufacturing",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Acme Corp"
        assert data["country"] == "CN"
        assert data["industry"] == "Manufacturing"
        assert data["follow_status"] == "new"
        assert data["grade"] is None
        assert data["tags"] == []
        assert "id" in data

    async def test_create_customer_empty_name(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "   "},
        )
        assert response.status_code == 422

    async def test_list_customers_empty(self, authenticated_client: AsyncClient):
        response = await authenticated_client.get("/api/v1/customers")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["page"] == 1
        assert data["page_size"] == 20

    async def test_list_customers_paginated(self, authenticated_client: AsyncClient):
        for i in range(3):
            await authenticated_client.post(
                "/api/v1/customers",
                json={"name": f"Customer {i}"},
            )

        response = await authenticated_client.get("/api/v1/customers?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2

    async def test_get_customer_detail(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Detail Corp", "website": "https://example.com"},
        )
        customer_id = create.json()["id"]

        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Detail Corp"
        assert data["website"] == "https://example.com"
        assert data["tags"] == []
        assert data["grade"] is None

    async def test_update_customer(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Old Name"},
        )
        customer_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/customers/{customer_id}",
            json={"name": "New Name", "country": "US"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["country"] == "US"

    async def test_delete_customer(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "To Delete"},
        )
        customer_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/customers/{customer_id}")
        assert response.status_code == 204

        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert response.status_code == 404

    async def test_get_customer_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.get(f"/api/v1/customers/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

    async def test_update_customer_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/customers/{fake_id}",
            json={"name": "Ghost Corp"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

    async def test_customer_with_grade(self, authenticated_client: AsyncClient):
        grade = await authenticated_client.post(
            "/api/v1/customer-grades",
            json={"name": "Platinum", "color": "#E5E4E2"},
        )
        grade_id = grade.json()["id"]

        create = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Platinum Customer", "grade_id": grade_id},
        )
        customer_id = create.json()["id"]

        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["grade_id"] == grade_id
        assert data["grade"] is not None
        assert data["grade"]["name"] == "Platinum"

    async def test_tag_and_untag_customer(self, authenticated_client: AsyncClient):
        tag = await authenticated_client.post("/api/v1/tags", json={"name": "vip"})
        tag_id = tag.json()["id"]

        customer = await authenticated_client.post(
            "/api/v1/customers",
            json={"name": "Tag Test Customer"},
        )
        customer_id = customer.json()["id"]

        # Tag the customer
        response = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/tags",
            json={"tag_id": tag_id},
        )
        assert response.status_code == 201

        detail = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        tags = detail.json()["tags"]
        assert any(t["id"] == tag_id for t in tags)

        # Untag
        response = await authenticated_client.delete(f"/api/v1/customers/{customer_id}/tags/{tag_id}")
        assert response.status_code == 204

        detail = await authenticated_client.get(f"/api/v1/customers/{customer_id}")
        assert detail.json()["tags"] == []


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


class TestContacts:
    async def _create_customer(self, client: AsyncClient) -> str:
        response = await client.post("/api/v1/customers", json={"name": "Contact Owner"})
        return response.json()["id"]

    async def test_create_contact(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        response = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert data["is_primary"] is True
        assert data["customer_id"] == customer_id

    async def test_create_second_contact_not_primary(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "First"},
        )
        response = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Second"},
        )
        assert response.status_code == 201
        assert response.json()["is_primary"] is False

    async def test_list_contacts(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Bob"},
        )
        response = await authenticated_client.get(f"/api/v1/customers/{customer_id}/contacts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bob"

    async def test_update_contact(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        create = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Charlie"},
        )
        contact_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/contacts/{contact_id}",
            json={"name": "Charlie Updated", "phone": "+1234567890"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Charlie Updated"
        assert data["phone"] == "+1234567890"

    async def test_set_primary_contact(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Primary"},
        )
        create2 = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "Secondary"},
        )
        contact2_id = create2.json()["id"]
        assert create2.json()["is_primary"] is False

        response = await authenticated_client.put(f"/api/v1/contacts/{contact2_id}/primary")
        assert response.status_code == 200
        assert response.json()["is_primary"] is True

    async def test_delete_contact(self, authenticated_client: AsyncClient):
        customer_id = await self._create_customer(authenticated_client)
        create = await authenticated_client.post(
            f"/api/v1/customers/{customer_id}/contacts",
            json={"name": "To Delete"},
        )
        contact_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/contacts/{contact_id}")
        assert response.status_code == 204

    async def test_create_contact_customer_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.post(
            f"/api/v1/customers/{fake_id}/contacts",
            json={"name": "Ghost"},
        )
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CUSTOMER_NOT_FOUND"

    async def test_delete_contact_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/contacts/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"]["code"] == "CONTACT_NOT_FOUND"
