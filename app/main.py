from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.config import settings
from app.core.db import postgres_db
from app.core.logging import setup_logging
from app.middlewares import LoggingMiddleware
from app.routes import notes, patients

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await postgres_db.init(settings.database_url)
    yield
    await postgres_db.close()


app = FastAPI(lifespan=lifespan, title=settings.app_name, debug=settings.debug)
app.add_middleware(LoggingMiddleware)
add_pagination(app)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(patients.router)
app.include_router(notes.router)
