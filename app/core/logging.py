import logging
import sys


def setup_logging() -> None:
    """Set up logging configuration for the application."""
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
