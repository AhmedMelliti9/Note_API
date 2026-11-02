"""Logging configuration for Notes API.

Configures structured logging using Python's standard logging module.
"""

import logging
import sys

LOGGER_NAME = "notes_api"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


# Default logger instance
logger = setup_logging()
