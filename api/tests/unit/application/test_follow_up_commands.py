from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from app.domain.customer.entities import Customer
from app.domain.customer.exceptions import CustomerNotFoundError
from app.domain.follow_up.entities import FollowUp
from app.domain.follow_up.enums import FollowUpMethod
from app.domain.follow_up.exceptions import FollowUpContentRequiredError


class TestCreateFollowUpHandler:
    @pytest.fixture
    def tenant_id(self) -> uuid.UUID:
        return uuid.uuid7()

    @pytest.fixture
    def user_id(self) -> uuid.UUID:
        return uuid.uuid7()

    @pytest.fixture
    def customer(self, tenant_id: uuid.UUID, user_id: uuid.UUID) -> Customer:
        return Customer.create(
            name="Test Customer",
            tenant_id=tenant_id,
            created_by=user_id,
        )

    @pytest.fixture
    def customer_repo(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def follow_up_repo(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def handler(
        self, follow_up_repo: AsyncMock, customer_repo: AsyncMock
    ) -> "CreateFollowUpHandler":
        from app.application.follow_up.commands import CreateFollowUpHandler
        from app.domain.follow_up.services import FollowUpService

        service = FollowUpService(follow_up_repo=follow_up_repo)
        return CreateFollowUpHandler(
            follow_up_service=service,
            customer_repo=customer_repo,
        )

    async def test_create_follow_up_success(
        self,
        handler: "CreateFollowUpHandler",
        customer: Customer,
        customer_repo: AsyncMock,
        follow_up_repo: AsyncMock,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        customer_repo.get_by_id.return_value = customer
        follow_up_repo.create.side_effect = lambda fu: fu

        result = await handler.handle(
            customer_id=customer.id,
            content="Sent quotation via email",
            method=FollowUpMethod.EMAIL,
            tenant_id=tenant_id,
            created_by=user_id,
        )

        assert result.content == "Sent quotation via email"
        assert result.method == FollowUpMethod.EMAIL
        assert result.customer_id == customer.id

        # Verify customer.last_follow_at was updated
        customer_repo.update.assert_awaited_once()
        updated_customer = customer_repo.update.call_args[0][0]
        assert updated_customer.last_follow_at is not None

    async def test_create_follow_up_customer_not_found(
        self,
        handler: "CreateFollowUpHandler",
        customer_repo: AsyncMock,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        customer_repo.get_by_id.return_value = None

        with pytest.raises(CustomerNotFoundError):
            await handler.handle(
                customer_id=uuid.uuid7(),
                content="Hello",
                method=FollowUpMethod.EMAIL,
                tenant_id=tenant_id,
                created_by=user_id,
            )

    async def test_create_follow_up_empty_content(
        self,
        handler: "CreateFollowUpHandler",
        customer: Customer,
        customer_repo: AsyncMock,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        customer_repo.get_by_id.return_value = customer

        with pytest.raises(FollowUpContentRequiredError):
            await handler.handle(
                customer_id=customer.id,
                content="   ",
                method=FollowUpMethod.EMAIL,
                tenant_id=tenant_id,
                created_by=user_id,
            )

    async def test_create_follow_up_with_all_fields(
        self,
        handler: "CreateFollowUpHandler",
        customer: Customer,
        customer_repo: AsyncMock,
        follow_up_repo: AsyncMock,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        customer_repo.get_by_id.return_value = customer
        follow_up_repo.create.side_effect = lambda fu: fu

        next_time = datetime(2026, 4, 1, tzinfo=UTC)
        result = await handler.handle(
            customer_id=customer.id,
            content="Discussed pricing details",
            method=FollowUpMethod.WECHAT,
            tenant_id=tenant_id,
            created_by=user_id,
            stage="negotiating",
            customer_response="Will consider",
            next_follow_at=next_time,
            tags=["urgent", "pricing"],
            attachment_urls=["https://s3.example.com/file.pdf"],
        )

        assert result.method == FollowUpMethod.WECHAT
        assert result.stage == "negotiating"
        assert result.customer_response == "Will consider"
        assert result.next_follow_at == next_time
        assert result.tags == ["urgent", "pricing"]
        assert result.attachment_urls == ["https://s3.example.com/file.pdf"]
