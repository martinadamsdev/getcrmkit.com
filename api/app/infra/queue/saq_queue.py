from typing import Any

from saq import Queue

from app.application.shared.task_queue import AbstractTaskQueue
from app.config.settings import get_settings


class SaqTaskQueue(AbstractTaskQueue):
    def __init__(self, queue: Queue) -> None:
        self._queue = queue

    @property
    def raw_queue(self) -> Queue:
        """Access the underlying SAQ Queue for worker configuration."""
        return self._queue

    async def enqueue(self, task_name: str, **kwargs: Any) -> None:
        await self._queue.enqueue(task_name, **kwargs)

    async def apply(self, task_name: str, *, timeout: int = 10, **kwargs: Any) -> Any:
        return await self._queue.apply(task_name, timeout=timeout, **kwargs)

    async def disconnect(self) -> None:
        await self._queue.disconnect()


def create_saq_queue() -> SaqTaskQueue:
    settings = get_settings()
    raw = Queue.from_url(settings.redis_url)
    return SaqTaskQueue(raw)


task_queue = create_saq_queue()
