from typing import Any

from app.config.settings import get_settings
from app.infra.queue import task_queue
from app.infra.queue.tasks import cron_jobs, task_functions

_settings = get_settings()


async def startup(ctx: dict[str, Any]) -> None:
    """Initialize resources shared across all tasks in this worker."""


async def shutdown(ctx: dict[str, Any]) -> None:
    """Clean up worker resources."""


settings: dict[str, Any] = {
    "queue": task_queue.raw_queue,
    "functions": task_functions,
    "cron_jobs": cron_jobs,
    "concurrency": _settings.worker_concurrency,
    "startup": startup,
    "shutdown": shutdown,
}
