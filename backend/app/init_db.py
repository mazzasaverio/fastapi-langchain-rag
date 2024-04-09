import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncpg
from app.core.config import settings
from app.crud import user_crud
from app.models.user_model import User, UserCreate
from dotenv import load_dotenv
from loguru import logger
import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlmodel import SQLModel, Session, create_engine, select


engine = create_async_engine(str(settings.ASYNC_DATABASE_URI), echo=True)


async def create_extension():
    conn: asyncpg.Connection = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASS,
        database=settings.DB_NAME,
        host=settings.DB_HOST,
    )
    try:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        logger.info("pgvector extension created or already exists.")
    except Exception as e:
        logger.error(f"Error creating pgvector extension: {e}")
    finally:
        await conn.close()


def create_database(database_name, user, password, host, port):
    try:
        # Connect to the default database
        conn = psycopg2.connect(
            dbname=database_name, user=user, password=password, host=host, port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if database exists
        cur.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'"
        )
        exists = cur.fetchone()
        if not exists:

            cur.execute(f"CREATE DATABASE {database_name}")
            logger.info(f"Database '{database_name}' created.")
        else:
            logger.info(f"Database '{database_name}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")


async def init_db() -> None:
    create_database(
        settings.DB_NAME,
        settings.DB_USER,
        settings.DB_PASS,
        settings.DB_HOST,
        settings.DB_PORT,
    )
    async with engine.begin() as conn:
        # Use run_sync to execute the create_all method in an asynchronous context
        await conn.run_sync(SQLModel.metadata.create_all)


def create_super_user() -> None:
    load_dotenv()

    FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

    engine = create_engine(str(settings.SYNC_DATABASE_URI))
    with Session(engine) as session:

        user = session.exec(select(User).where(User.email == FIRST_SUPERUSER)).first()
        if not user:
            user_in = UserCreate(
                email=FIRST_SUPERUSER,
                password=FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = user_crud.create_user(session=session, user_create=user_in)


if __name__ == "__main__":

    asyncio.run(init_db())

    create_super_user()
