import uuid

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TestScriptTemplatesCRUD:
    async def test_list_templates_empty(self, authenticated_client: AsyncClient):
        response = await authenticated_client.get("/api/v1/script-templates")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_template(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/script-templates",
            json={
                "scene": "first_contact",
                "title": "Initial Outreach",
                "content": "Hello, I am writing to introduce...",
                "language": "en",
                "position": 1,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["scene"] == "first_contact"
        assert data["title"] == "Initial Outreach"
        assert data["content"] == "Hello, I am writing to introduce..."
        assert data["language"] == "en"
        assert data["position"] == 1
        assert data["is_system"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_template_defaults(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/script-templates",
            json={
                "scene": "follow_up",
                "title": "Follow Up",
                "content": "Just checking in...",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["language"] == "zh-CN"
        assert data["position"] == 0

    async def test_create_template_empty_title_422(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/script-templates",
            json={
                "scene": "first_contact",
                "title": "   ",
                "content": "some content",
            },
        )
        assert response.status_code == 422

    async def test_list_templates_includes_created(self, authenticated_client: AsyncClient):
        await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "quotation", "title": "Quote Template", "content": "Dear customer..."},
        )
        await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "sample", "title": "Sample Follow-up", "content": "Your sample has shipped..."},
        )
        response = await authenticated_client.get("/api/v1/script-templates")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_filter_by_scene(self, authenticated_client: AsyncClient):
        await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "quotation", "title": "Q1", "content": "content1"},
        )
        await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "sample", "title": "S1", "content": "content2"},
        )
        response = await authenticated_client.get("/api/v1/script-templates?scene=quotation")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["scene"] == "quotation"

    async def test_update_template(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "first_contact", "title": "Original", "content": "original content"},
        )
        template_id = create.json()["id"]

        response = await authenticated_client.put(
            f"/api/v1/script-templates/{template_id}",
            json={"title": "Updated Title", "content": "updated content"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "updated content"

    async def test_update_template_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.put(
            f"/api/v1/script-templates/{fake_id}",
            json={"title": "Updated"},
        )
        assert response.status_code == 404

    async def test_delete_user_template(self, authenticated_client: AsyncClient):
        create = await authenticated_client.post(
            "/api/v1/script-templates",
            json={"scene": "first_contact", "title": "To Delete", "content": "delete me"},
        )
        template_id = create.json()["id"]

        response = await authenticated_client.delete(f"/api/v1/script-templates/{template_id}")
        assert response.status_code == 204

        # Verify it's gone
        list_response = await authenticated_client.get("/api/v1/script-templates")
        assert all(t["id"] != template_id for t in list_response.json())

    async def test_delete_template_not_found(self, authenticated_client: AsyncClient):
        fake_id = str(uuid.uuid4())
        response = await authenticated_client.delete(f"/api/v1/script-templates/{fake_id}")
        assert response.status_code == 404

    async def test_delete_system_template_forbidden(
        self, authenticated_client_with_session: tuple[AsyncClient, AsyncSession]
    ):
        """System templates (is_system=True) cannot be deleted — 403."""
        import uuid as uuid_mod
        from datetime import UTC, datetime

        from app.infra.database.models.follow_up import ScriptTemplateModel
        from app.infra.database.models.user import UserModel

        client, session = authenticated_client_with_session

        # Look up the test user's tenant_id from the DB session
        stmt = select(UserModel).where(UserModel.email == "test-session@example.com")
        result = await session.execute(stmt)
        user = result.scalar_one()

        # Insert a system template directly into the same DB session
        system_template = ScriptTemplateModel(
            id=uuid_mod.uuid7(),
            tenant_id=user.tenant_id,
            scene="first_contact",
            title="System Template",
            content="System content",
            language="zh-CN",
            position=0,
            is_system=True,
            created_by=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        session.add(system_template)
        await session.flush()

        response = await client.delete(f"/api/v1/script-templates/{system_template.id}")
        assert response.status_code == 403
        assert response.json()["detail"]["code"] == "SYSTEM_TEMPLATE_PROTECTED"
