from pydantic_settings import BaseSettings
from typing import List
from loguru import logger
from typing import Annotated, Any, Literal
import sys
import secrets

from pydantic import (
    AnyUrl,
    BeforeValidator,
)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):

    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    PROJECT_NAME: str

    SECRET_KEY: str = secrets.token_urlsafe(32)

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASS: str
    DB_USER: str

    OPENAI_API_KEY: str
    OPENAI_ORGANIZATION: str

    REDIS_HOST: str
    REDIS_PORT: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    BACKEND_CORS_ORIGINS: List[str] = []

    @property
    def ASYNC_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URI(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = "../.env"


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
