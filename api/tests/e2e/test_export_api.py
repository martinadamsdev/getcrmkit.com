from httpx import AsyncClient


class TestExportCustomers:
    async def test_export_customers(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post("/api/v1/customers/export")
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data

        # Verify the job exists via data-jobs endpoint
        job_id = data["job_id"]
        job_response = await authenticated_client.get(f"/api/v1/data-jobs/{job_id}")
        assert job_response.status_code == 200
        job_data = job_response.json()
        assert job_data["job_type"] == "export"
        assert job_data["status"] == "pending"

    async def test_export_with_filter(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/customers/export",
            json={"filter_config": {"source": "alibaba"}},
        )
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data

    async def test_export_unauthenticated(self, client: AsyncClient):
        response = await client.post("/api/v1/customers/export")
        assert response.status_code == 401
