import logging
import sys

from src.utils.config import get_settings


def setup_logger(name: str = "resume_job_matcher") -> logging.Logger:
    """
    Create and configure the application logger.

    The logger writes structured, timestamped messages to stdout.
    """

    settings = get_settings()

    logger = logging.getLogger(name)

    # Prevent duplicate handlers when setup_logger() is called
    # multiple times.
    if logger.handlers:
        return logger

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Avoid sending messages to the root logger.
    logger.propagate = False

    return logger


logger = setup_logger()