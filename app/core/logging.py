import logging
import sys

from app.config import settings


def setup_logging() -> None:
    """Set up logging configuration for the application."""
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
