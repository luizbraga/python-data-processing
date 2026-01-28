from fastapi import FastAPI

from app.config import settings
from app.core.logging import setup_logging
from app.routes import patients

setup_logging()

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(patients.router)
