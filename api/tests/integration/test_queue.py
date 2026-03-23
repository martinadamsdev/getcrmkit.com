import asyncio

from saq import Worker

from app.infra.queue.saq_queue import create_saq_queue
from app.infra.queue.tasks import task_functions


async def test_saq_queue_connects_to_redis() -> None:
    """Verify the SAQ queue can connect to Redis and report info."""
    queue = create_saq_queue()
    info = await queue.raw_queue.info()
    assert "workers" in info
    await queue.disconnect()


async def test_enqueue_and_process_ping() -> None:
    """End-to-end: enqueue a ping task, run an in-process worker, verify result."""
    queue = create_saq_queue()
    worker = Worker(queue.raw_queue, functions=task_functions)

    async def run_worker() -> None:
        await worker.start()

    worker_task = asyncio.create_task(run_worker())

    try:
        result = await queue.apply("ping", timeout=5)
        assert result == {"pong": True}
    finally:
        await worker.stop()
        await worker_task
        await queue.disconnect()
