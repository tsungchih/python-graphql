import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.1.0"

config = Config("/app/app/.env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
#logger.add("file_{time}.log", rotation="1 day", compression="tar.gz", retention="1 week")