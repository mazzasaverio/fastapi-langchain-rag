from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(
    DB_POOL_SIZE // WEB_CONCURRENCY,
    5,
)


def _get_local_session() -> sessionmaker:
    engine = (
        create_async_engine(
            url=settings.ASYNC_DATABASE_URI,
            future=True,
            pool_size=POOL_SIZE,
            max_overflow=64,
        )
        if settings.ASYNC_DATABASE_URI is not None
        else None
    )
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


SessionLocal = _get_local_session()
