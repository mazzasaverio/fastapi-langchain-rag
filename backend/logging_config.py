from loguru import logger
import sys

def setup_logging():
    logger.remove()  # Remove default handler
    # Configure Loguru logger to output to stderr with the desired format and level
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>", level="DEBUG")

# Call the setup function to ensure logging is configured when the module is imported
setup_logging()
