import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.entities import Customer
from app.domain.customer.enums import FollowUpStage
from app.domain.follow_up.entities import FollowUp, ScriptTemplate
from app.domain.follow_up.enums import FollowUpMethod, ScriptScene
from app.infra.database.models.user import UserModel
from app.infra.database.repositories.customer_repository import CustomerRepository
from app.infra.database.repositories.follow_up_repository import (
    FollowUpRepository,
    ScriptTemplateRepository,
)


async def create_test_user(session: AsyncSession, tenant_id: uuid.UUID) -> uuid.UUID:
    """Create a minimal user row to satisfy FK constraints."""
    now = datetime.now(UTC)
    user_id = uuid.uuid7()
    user = UserModel(
        id=user_id,
        tenant_id=tenant_id,
        email=f"test-{user_id}@example.com",
        password_hash="hashed",
        name="Test User",
        created_at=now,
        updated_at=now,
    )
    session.add(user)
    await session.flush()
    return user_id


def make_customer(tenant_id: uuid.UUID, name: str = "Test Corp") -> Customer:
    now = datetime.now(UTC)
    return Customer(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        name=name,
        follow_status=FollowUpStage.NEW,
        custom_fields={},
        created_at=now,
        updated_at=now,
    )


def make_follow_up(
    tenant_id: uuid.UUID,
    customer_id: uuid.UUID,
    content: str = "Test follow-up",
    method: FollowUpMethod = FollowUpMethod.EMAIL,
    **kwargs: object,
) -> FollowUp:
    now = datetime.now(UTC)
    return FollowUp(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        customer_id=customer_id,
        method=method,
        content=content,
        tags=kwargs.get("tags", []),  # type: ignore[arg-type]
        next_follow_at=kwargs.get("next_follow_at"),  # type: ignore[arg-type]
        attachment_urls=kwargs.get("attachment_urls", []),  # type: ignore[arg-type]
        created_by=kwargs.get("created_by"),  # type: ignore[arg-type]
        created_at=now,
        updated_at=now,
    )


def make_template(
    tenant_id: uuid.UUID,
    title: str = "Test Template",
    scene: ScriptScene = ScriptScene.FIRST_CONTACT,
    **kwargs: object,
) -> ScriptTemplate:
    now = datetime.now(UTC)
    return ScriptTemplate(
        id=uuid.uuid7(),
        tenant_id=tenant_id,
        scene=scene,
        title=title,
        content=kwargs.get("content", "Template content"),  # type: ignore[arg-type]
        language=kwargs.get("language", "zh-CN"),  # type: ignore[arg-type]
        position=kwargs.get("position", 0),  # type: ignore[arg-type]
        is_system=kwargs.get("is_system", False),  # type: ignore[arg-type]
        created_by=kwargs.get("created_by"),  # type: ignore[arg-type]
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------------------------
# FollowUpRepository
# ---------------------------------------------------------------------------


class TestFollowUpRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        follow_up = make_follow_up(tenant_id, customer.id)
        created = await repo.create(follow_up)

        fetched = await repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.content == "Test follow-up"
        assert fetched.customer_id == customer.id

    async def test_get_by_id_not_found(self, db_session: AsyncSession) -> None:
        repo = FollowUpRepository(db_session)
        result = await repo.get_by_id(uuid.uuid7(), uuid.uuid7())
        assert result is None

    async def test_get_by_customer_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        for i in range(3):
            await repo.create(make_follow_up(tenant_id, customer.id, content=f"Follow-up {i}"))

        items, total = await repo.get_by_customer_id(tenant_id, customer.id)
        assert total == 3
        assert len(items) == 3

    async def test_get_by_tenant_with_tags_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        await repo.create(make_follow_up(tenant_id, customer.id, content="Tagged", tags=["vip", "urgent"]))
        await repo.create(make_follow_up(tenant_id, customer.id, content="No tags"))

        items, total = await repo.get_by_tenant(tenant_id, tags=["vip"])
        assert total == 1
        assert items[0].content == "Tagged"

    async def test_update(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        follow_up = await repo.create(make_follow_up(tenant_id, customer.id))

        follow_up.content = "Updated content"
        follow_up.updated_at = datetime.now(UTC)
        updated = await repo.update(follow_up)
        assert updated.content == "Updated content"

    async def test_soft_delete(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        follow_up = await repo.create(make_follow_up(tenant_id, customer.id))

        await repo.soft_delete(tenant_id, follow_up.id)

        result = await repo.get_by_id(tenant_id, follow_up.id)
        assert result is None

    async def test_find_due_reminders(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        past = datetime.now(UTC) - timedelta(hours=1)
        future = datetime.now(UTC) + timedelta(hours=1)

        await repo.create(make_follow_up(tenant_id, customer.id, content="Due", next_follow_at=past))
        await repo.create(make_follow_up(tenant_id, customer.id, content="Not due", next_follow_at=future))
        await repo.create(make_follow_up(tenant_id, customer.id, content="No reminder"))

        due = await repo.find_due_reminders(before=datetime.now(UTC))
        assert len(due) == 1
        assert due[0].content == "Due"

    async def test_get_by_tenant_with_created_by_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        user_id = await create_test_user(db_session, tenant_id)
        customer_repo = CustomerRepository(db_session)
        customer = await customer_repo.create(make_customer(tenant_id))

        repo = FollowUpRepository(db_session)
        await repo.create(make_follow_up(tenant_id, customer.id, content="Mine", created_by=user_id))
        await repo.create(make_follow_up(tenant_id, customer.id, content="Others"))

        items, total = await repo.get_by_tenant(tenant_id, created_by=user_id)
        assert total == 1
        assert items[0].content == "Mine"


# ---------------------------------------------------------------------------
# ScriptTemplateRepository
# ---------------------------------------------------------------------------


class TestScriptTemplateRepository:
    async def test_create_and_get_by_id(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        tpl = make_template(tenant_id)
        created = await repo.create(tpl)

        fetched = await repo.get_by_id(tenant_id, created.id)
        assert fetched is not None
        assert fetched.title == "Test Template"

    async def test_get_all(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        await repo.create(make_template(tenant_id, title="A", position=1))
        await repo.create(make_template(tenant_id, title="B", position=0))

        templates = await repo.get_all(tenant_id)
        assert len(templates) == 2
        assert templates[0].title == "B"  # sorted by position

    async def test_get_all_with_scene_filter(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        await repo.create(make_template(tenant_id, title="A", scene=ScriptScene.FIRST_CONTACT))
        await repo.create(make_template(tenant_id, title="B", scene=ScriptScene.QUOTATION))

        templates = await repo.get_all(tenant_id, scene="first_contact")
        assert len(templates) == 1
        assert templates[0].title == "A"

    async def test_update(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        tpl = await repo.create(make_template(tenant_id))

        tpl.title = "Updated Title"
        tpl.updated_at = datetime.now(UTC)
        updated = await repo.update(tpl)
        assert updated.title == "Updated Title"

    async def test_delete(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        tpl = await repo.create(make_template(tenant_id))

        await repo.delete(tenant_id, tpl.id)

        result = await repo.get_by_id(tenant_id, tpl.id)
        assert result is None

    async def test_count_by_tenant(self, db_session: AsyncSession) -> None:
        tenant_id = uuid.uuid7()
        repo = ScriptTemplateRepository(db_session)
        await repo.create(make_template(tenant_id, title="A"))
        await repo.create(make_template(tenant_id, title="B"))

        count = await repo.count_by_tenant(tenant_id)
        assert count == 2
