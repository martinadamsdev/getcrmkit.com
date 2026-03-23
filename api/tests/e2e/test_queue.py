from httpx import AsyncClient


async def test_health_still_works_with_queue_lifespan(client: AsyncClient) -> None:
    """Verify the app starts correctly with queue lifespan wired in."""
    response = await client.get("/health")
    assert response.status_code == 200
