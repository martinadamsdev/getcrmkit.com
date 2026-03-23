import io

from httpx import AsyncClient
from openpyxl import Workbook


def _make_xlsx() -> io.BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.append(["name", "country", "source"])
    ws.append(["Test Corp", "US", "alibaba"])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


class TestImportCustomers:
    async def test_import_xlsx(self, authenticated_client: AsyncClient):
        buf = _make_xlsx()
        response = await authenticated_client.post(
            "/api/v1/customers/import",
            files={
                "file": ("customers.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            },
        )
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data

        # Verify the job exists via data-jobs endpoint
        job_id = data["job_id"]
        job_response = await authenticated_client.get(f"/api/v1/data-jobs/{job_id}")
        assert job_response.status_code == 200
        job_data = job_response.json()
        assert job_data["job_type"] == "import"
        assert job_data["status"] == "pending"
        assert job_data["file_name"] == "customers.xlsx"

    async def test_import_invalid_file(self, authenticated_client: AsyncClient):
        buf = io.BytesIO(b"not a spreadsheet")
        response = await authenticated_client.post(
            "/api/v1/customers/import",
            files={"file": ("customers.txt", buf, "text/plain")},
        )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "INVALID_IMPORT_FILE"

    async def test_import_unauthenticated(self, client: AsyncClient):
        buf = _make_xlsx()
        response = await client.post(
            "/api/v1/customers/import",
            files={
                "file": ("customers.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            },
        )
        assert response.status_code == 401
