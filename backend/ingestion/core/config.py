from pydantic_settings import BaseSettings
from typing import List
from loguru import logger
import sys


class Settings(BaseSettings):

    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASS: str
    DB_USER: str

    OPENAI_API_KEY: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    @property
    def ASYNC_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


class LogConfig:
    LOGGING_LEVEL = "DEBUG"
    LOGGING_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"

    @staticmethod
    def configure_logging():
        logger.remove()

        logger.add(
            sys.stderr, format=LogConfig.LOGGING_FORMAT, level=LogConfig.LOGGING_LEVEL
        )


LogConfig.configure_logging()

settings = Settings()
