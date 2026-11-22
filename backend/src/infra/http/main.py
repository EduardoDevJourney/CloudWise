from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infra.config import get_settings
from infra.events.subscribers.logging_subscriber import register_subscribers
from infra.http.controllers.auth_controller import router as auth_router
from infra.http.controllers.cloudwise_controller import router as cloudwise_router
from infra.http.controllers.health_controller import router as health_router
from infra.http.controllers.runops_controller import router as runops_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    register_subscribers()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Cloud Wise API", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(runops_router, prefix="/api/v1")
    app.include_router(cloudwise_router, prefix="/api/v1")
    return app


app = create_app()
