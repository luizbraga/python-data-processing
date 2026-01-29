from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.config import settings
from app.core.logging import setup_logging
from app.routes import patients

setup_logging()

app = FastAPI(title=settings.app_name, debug=settings.debug)
add_pagination(app)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(patients.router)
