from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
import asyncpg
import psycopg2
from loguru import logger

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

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

    # Your existing database initialization logic here
    # For example, creating extensions or setting up initial data
    await create_extension()
    logger.info("Database initialized and all tables created if they didn't exist.")
