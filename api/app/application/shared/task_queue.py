from abc import ABC, abstractmethod
from typing import Any


class AbstractTaskQueue(ABC):
    @abstractmethod
    async def enqueue(self, task_name: str, **kwargs: Any) -> None:
        """Enqueue a task for background processing."""
        ...

    @abstractmethod
    async def apply(self, task_name: str, *, timeout: int = 10, **kwargs: Any) -> Any:
        """Enqueue a task and wait for its result."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the queue connection."""
        ...
