from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra.queue import task_queue
from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.system import router as system_router


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
    return app


app = create_app()
