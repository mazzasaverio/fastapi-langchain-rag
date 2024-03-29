import sys
import os

# Temporary solution.It is used to predict the centralization of logs in the future
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import yaml
import os

from dotenv import load_dotenv
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import CacheBackedEmbeddings
from backend.logging_config import logger


# from helpers.embedding_models import get_embedding_model

load_dotenv()

ingestion_config = yaml.load(
    open("backend/ingestion/config.yaml"), Loader=yaml.FullLoader
)

path_raw_pdf = ingestion_config.get("PATH_RAW_PDF", None)
collection_name = ingestion_config.get("COLLECTION_NAME", None)
db_name = os.getenv("DB_NAME")

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


class PDFExtractionPipeline:
    """Pipeline for extracting text from PDFs and loading them into a vector store."""

    db: PGVector | None = None
    embedding: CacheBackedEmbeddings

    def __init__(self):
        logger.info("Initializing PDFExtractionPipeline")
        # self.embedding_model = get_embedding_model()

        self.connection_str = PGVector.connection_string_from_db_params(
            driver="psycopg2",
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=db_name,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
        )
        logger.debug(f"Connection string: {self.connection_str}")

    def run(self, collection_name: str):
        logger.info(f"Running extraction pipeline for collection: {collection_name}")
        # Example method to demonstrate usage
        pass


# Example usage
if __name__ == "__main__":
    logger.info("Starting PDF extraction pipeline")
    pipeline = PDFExtractionPipeline()
    pipeline.run(collection_name)
