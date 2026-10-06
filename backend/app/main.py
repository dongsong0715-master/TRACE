from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.auth import router
from app.core.config import Settings
from app.core.database import create_database
from app.core.errors import error_response, install_error_handlers, success
from app.schemas.responses import Envelope, HealthOut


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    engine, factory = create_database(config)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        engine.dispose()

    app = FastAPI(title="TRACE API", version="0.1.0", lifespan=lifespan)
    app.state.settings, app.state.engine, app.state.session_factory = config, engine, factory
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.public_origin],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "PUT"],
        allow_headers=["Content-Type"],
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request.state.request_id = str(uuid4())
        if request.method in {"POST", "PATCH", "PUT", "DELETE"} and (
            request.headers.get("origin") != config.public_origin
        ):
            response = error_response(request, 403, "ORIGIN_REJECTED", "请求来源不受信任")
        else:
            response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    install_error_handlers(app)
    app.include_router(router, prefix="/api/v1")

    @app.get("/api/v1/health", tags=["system"], response_model=Envelope[HealthOut])
    def health(request: Request):
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.execute(text("SELECT id FROM users LIMIT 0"))
        return success(request, {"status": "ok", "version": "0.1.0", "database": "connected"})

    return app
