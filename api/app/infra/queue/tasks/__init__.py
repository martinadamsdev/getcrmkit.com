from collections.abc import Callable
from typing import Any

from app.infra.queue.tasks.customer_tasks import process_customer_export, process_customer_import
from app.infra.queue.tasks.example import ping
from app.infra.queue.tasks.follow_up_tasks import check_follow_up_reminders, follow_up_cron_jobs
from app.infra.queue.tasks.product_tasks import process_product_export, process_product_import

task_functions: list[Callable[..., Any]] = [
    ping,
    process_customer_import,
    process_customer_export,
    check_follow_up_reminders,
    process_product_import,
    process_product_export,
]

cron_jobs = [*follow_up_cron_jobs]
