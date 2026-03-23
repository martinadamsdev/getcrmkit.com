from httpx import AsyncClient


class TestCustomerFilter:
    async def _seed_customers(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/customers",
            json={"name": "Acme Corp", "source": "alibaba", "country": "US", "industry": "Manufacturing"},
        )
        await client.post(
            "/api/v1/customers",
            json={"name": "Beta Inc", "source": "alibaba", "country": "CN", "industry": "Tech"},
        )
        await client.post(
            "/api/v1/customers",
            json={"name": "Gamma Ltd", "source": "exhibition", "country": "US", "industry": "Manufacturing"},
        )

    async def test_filter_by_source(self, authenticated_client: AsyncClient):
        await self._seed_customers(authenticated_client)
        response = await authenticated_client.get("/api/v1/customers?source=alibaba")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        sources = {item["source"] for item in data["items"]}
        assert sources == {"alibaba"}

    async def test_filter_by_keyword(self, authenticated_client: AsyncClient):
        await self._seed_customers(authenticated_client)
        response = await authenticated_client.get("/api/v1/customers?keyword=Acme")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        names = [item["name"] for item in data["items"]]
        assert "Acme Corp" in names

    async def test_filter_by_source_and_country(self, authenticated_client: AsyncClient):
        await self._seed_customers(authenticated_client)
        response = await authenticated_client.get("/api/v1/customers?source=alibaba&country=US")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Acme Corp"

    async def test_sort_by_name_asc(self, authenticated_client: AsyncClient):
        await self._seed_customers(authenticated_client)
        response = await authenticated_client.get("/api/v1/customers?sort_by=name&sort_order=asc")
        assert response.status_code == 200
        data = response.json()
        names = [item["name"] for item in data["items"]]
        assert names == sorted(names)

    async def test_filter_unauthenticated(self, client: AsyncClient):
        response = await client.get("/api/v1/customers?source=alibaba")
        assert response.status_code == 401
