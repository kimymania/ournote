"""
Experimenting with logging modules - not implemented yet
"""

import logging
import time
from pathlib import Path
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_filename = "app.log"
log_path = log_dir / log_filename

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        # Log request details
        client_ip = request.client.host  # type: ignore
        method = request.method
        url = request.url.path

        start_time = time.perf_counter()
        logger.info(f"Request: [{start_time}] {method} {url} from {client_ip}")

        # Process the request
        response = await call_next(request)
        end_time = time.perf_counter()
        process_dt = end_time - start_time

        # Log response details
        status_code = response.status_code
        logger.info(
            f"Response: [{end_time}] {method} {url} returned {status_code} to {client_ip} in {process_dt}s"
        )

        return response
