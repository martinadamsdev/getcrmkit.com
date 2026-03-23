from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra.queue import task_queue
from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.contacts import router as contacts_router
from app.interfaces.api.v1.customer_grades import router as customer_grades_router
from app.interfaces.api.v1.customers import router as customers_router
from app.interfaces.api.v1.system import router as system_router
from app.interfaces.api.v1.tags import customer_tags_router
from app.interfaces.api.v1.tags import router as tags_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield
    await task_queue.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Get CRM Kit API",
        description="Open-source CRM for international trade SOHO",
        version="0.2.0",
        lifespan=lifespan,
    )
    app.include_router(system_router)
    app.include_router(auth_router)
    app.include_router(customer_grades_router)
    app.include_router(tags_router)
    app.include_router(customer_tags_router)
    app.include_router(customers_router)
    app.include_router(contacts_router)
    return app


app = create_app()
