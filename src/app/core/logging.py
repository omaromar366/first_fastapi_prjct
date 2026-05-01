from pathlib import Path
import sys

from loguru import logger

from app.core.config import settings

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


def setup_logging():
    logger.remove()

    if settings.app_env == "prod":
        logger.add(
            sys.stdout,
            level=settings.log_level,
            serialize=True,
            enqueue=True,
        )
    else:
        fmt = (
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level:<8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
            "<level>{message}</level>"
        )

        logger.add(
            sys.stdout,
            level=settings.log_level,
            format=fmt,
        )

    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        level=settings.log_level,
        serialize=(settings.app_env == "prod"),
    )

    return logger
