import sys

from loguru import logger

from src.config.settings import settings


def configure_logger() -> None:

    settings.LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        colorize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        settings.APPLICATION_LOG,
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        encoding="utf-8",
    )

    logger.add(
        settings.QUALITY_LOG,
        level="INFO",
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        enqueue=True,
        backtrace=False,
        diagnose=False,
        encoding="utf-8",
        filter=lambda record: record["extra"].get("quality", False),
    )


def get_logger():
    return logger


def get_quality_logger():
    return logger.bind(quality=True)
