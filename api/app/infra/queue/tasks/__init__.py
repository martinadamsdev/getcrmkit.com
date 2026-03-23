from collections.abc import Callable
from typing import Any

from app.infra.queue.tasks.example import ping

task_functions: list[Callable[..., Any]] = [ping]
