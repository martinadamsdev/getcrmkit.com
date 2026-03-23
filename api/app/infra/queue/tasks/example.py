from typing import Any


async def ping(ctx: dict[str, Any]) -> dict[str, bool]:
    """Health-check task to verify the worker processes jobs."""
    return {"pong": True}
