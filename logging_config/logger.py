import os
from datetime import datetime
from loguru import logger

from config.settings import Settings


def setup_logger(settings: Settings | None = None) -> logger:
    """Configure loguru logger with file and console handlers."""
    # Remove default handler
    logger.remove()

    # Console handler
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format=console_format,
        level="INFO",
        colorize=True,
    )

    # File handler with rotation
    log_dir = "reports/logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir, f"framework_{datetime.now().strftime('%Y%m%d')}.log"
    )

    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name} | "
        "{function}:{line} | "
        "{message}"
    )
    logger.add(
        sink=log_file,
        format=file_format,
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
        compression="zip",
    )

    if settings:
        logger.info(f"Logger initialized. Log file: {log_file}")

    return logger


def get_logger(name: str):
    """Get a named logger instance."""
    return logger.bind(name=name)
