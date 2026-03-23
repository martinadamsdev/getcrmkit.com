from app.application.shared.task_queue import AbstractTaskQueue
from app.infra.queue.saq_queue import SaqTaskQueue, create_saq_queue
from app.infra.queue.tasks import task_functions
from app.infra.queue.tasks.example import ping


def test_saq_queue_implements_abstract_task_queue() -> None:
    queue = create_saq_queue()
    assert isinstance(queue, AbstractTaskQueue)


def test_create_saq_queue_returns_instance() -> None:
    queue = create_saq_queue()
    assert isinstance(queue, SaqTaskQueue)


async def test_ping_task_returns_pong() -> None:
    result = await ping({"job": None})
    assert result == {"pong": True}


def test_task_functions_includes_ping() -> None:
    assert ping in task_functions
