import logging
import time
from typing import Any, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response | Any:
        start_time = time.time()

        host = request.client.host if request.client else "unknown"

        # Log request
        logger.info(f"Request: ({host}) {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            logger.info(
                f"Response: ({host}) {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Duration: {process_time:.4f}s"
            )

            response.headers["X-Process-Time"] = str(process_time)
            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: ({host}) {request.method} {request.url.path} "
                f"Exception: {str(e)} "
                f"Duration: {process_time:.4f}s"
            )
            raise
