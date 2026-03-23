from httpx import AsyncClient


class TestFollowUpReport:
    async def _create_customer(self, client: AsyncClient) -> str:
        response = await client.post("/api/v1/customers", json={"name": "Report Test Customer"})
        assert response.status_code == 201
        return response.json()["id"]

    async def _create_follow_up(
        self, client: AsyncClient, customer_id: str, method: str = "email", content: str = "Test follow-up"
    ) -> dict:
        response = await client.post(
            "/api/v1/follow-ups",
            json={
                "customer_id": customer_id,
                "method": method,
                "content": content,
            },
        )
        assert response.status_code == 201
        return response.json()

    async def test_report_daily_empty(self, authenticated_client: AsyncClient):
        """GET /follow-ups/report?period=daily returns valid structure even with no data."""
        response = await authenticated_client.get("/api/v1/follow-ups/report?period=daily")
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "daily"
        assert "start_date" in data
        assert "end_date" in data
        assert data["total"] == 0
        assert data["items"] == []

    async def test_report_weekly_empty(self, authenticated_client: AsyncClient):
        """GET /follow-ups/report?period=weekly returns valid structure."""
        response = await authenticated_client.get("/api/v1/follow-ups/report?period=weekly")
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "weekly"
        assert data["total"] == 0

    async def test_report_monthly_empty(self, authenticated_client: AsyncClient):
        """GET /follow-ups/report?period=monthly returns valid structure."""
        response = await authenticated_client.get("/api/v1/follow-ups/report?period=monthly")
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "monthly"

    async def test_report_yearly_empty(self, authenticated_client: AsyncClient):
        """GET /follow-ups/report?period=yearly returns valid structure."""
        response = await authenticated_client.get("/api/v1/follow-ups/report?period=yearly")
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "yearly"

    async def test_report_default_period_is_daily(self, authenticated_client: AsyncClient):
        """GET /follow-ups/report without period param defaults to daily."""
        response = await authenticated_client.get("/api/v1/follow-ups/report")
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "daily"

    async def test_report_with_follow_up_data(self, authenticated_client: AsyncClient):
        """Report counts match the number of created follow-ups."""
        customer_id = await self._create_customer(authenticated_client)

        # Create 3 follow-ups today
        for i in range(3):
            await self._create_follow_up(authenticated_client, customer_id, content=f"Report test {i}")

        response = await authenticated_client.get("/api/v1/follow-ups/report?period=daily")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 1  # All created today, so 1 bucket
        assert data["items"][0]["total_count"] == 3

    async def test_report_method_breakdown(self, authenticated_client: AsyncClient):
        """Report correctly breaks down follow-ups by method."""
        customer_id = await self._create_customer(authenticated_client)

        # Create follow-ups with different methods
        await self._create_follow_up(authenticated_client, customer_id, method="email", content="Email follow-up")
        await self._create_follow_up(authenticated_client, customer_id, method="email", content="Email follow-up 2")
        await self._create_follow_up(authenticated_client, customer_id, method="wechat", content="WeChat follow-up")
        await self._create_follow_up(authenticated_client, customer_id, method="alibaba", content="Alibaba follow-up")

        response = await authenticated_client.get("/api/v1/follow-ups/report?period=daily")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 4
        assert len(data["items"]) == 1

        breakdown = data["items"][0]["method_breakdown"]
        assert breakdown["email"] == 2
        assert breakdown["wechat"] == 1
        assert breakdown["alibaba"] == 1

    async def test_report_weekly_includes_today(self, authenticated_client: AsyncClient):
        """Weekly report includes follow-ups created today."""
        customer_id = await self._create_customer(authenticated_client)
        await self._create_follow_up(authenticated_client, customer_id, content="This week")

        response = await authenticated_client.get("/api/v1/follow-ups/report?period=weekly")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    async def test_report_requires_auth(self, client: AsyncClient):
        """Report endpoint requires authentication."""
        response = await client.get("/api/v1/follow-ups/report?period=daily")
        assert response.status_code == 401
