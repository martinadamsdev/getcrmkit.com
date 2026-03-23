from fastapi import FastAPI

from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.system import router as system_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="CRMKit API",
        description="Open-source CRM for international trade SOHO",
        version="0.2.0",
    )
    app.include_router(system_router)
    app.include_router(auth_router)
    return app


app = create_app()
