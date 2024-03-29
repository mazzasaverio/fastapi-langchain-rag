from loguru import logger
import sys


def setup_logging():
    logger.remove()

    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
        level="DEBUG",
    )


setup_logging()
