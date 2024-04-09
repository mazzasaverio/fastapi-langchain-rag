import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
import json
from typing import Any, List
from langchain.schema import Document

from dotenv import load_dotenv

from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import CacheBackedEmbeddings
from app.core.config import logger
from app.schemas.ingestion_schema import LOADER_DICT
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from utils.embedding_models import get_embedding_model
from langchain.text_splitter import TokenTextSplitter
from backend.app.init_db import engine, init_db
from backend.app.init_db import create_super_user

load_dotenv()

ingestion_config_path = os.path.join(
    os.path.dirname(__file__), "..", "config/ingestion.yml"
)

ingestion_config = yaml.load(
    open(ingestion_config_path, "r"),
    Loader=yaml.FullLoader,
)

path_input_folder = ingestion_config.get("PATH_RAW_PDF", None)
collection_name = ingestion_config.get("COLLECTION_NAME", None)
path_extraction_folder = ingestion_config.get("PATH_EXTRACTION", None)


pdf_parser = ingestion_config.get("PDF_PARSER", None)

chunk_size = ingestion_config.get("TOKENIZER_CHUNK_SIZE", None)
chunk_overlap = ingestion_config.get("TOKENIZER_CHUNK_OVERLAP", None)

db_name = os.getenv("DB_NAME")

DATABASE_HOST = os.getenv("DB_HOST")
DATABASE_PORT = os.getenv("DB_PORT")
DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASS")


class PDFExtractionPipeline:
    """Pipeline for extracting text from PDFs and loading them into a vector store."""

    db: PGVector | None = None
    embedding: CacheBackedEmbeddings

    def __init__(self):
        logger.info("Initializing PDFExtractionPipeline")

        self.pdf_loader = LOADER_DICT[pdf_parser]
        self.embedding_model = get_embedding_model()

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

        self._load_documents(
            folder_path=path_input_folder, collection_name=collection_name
        )

    def _load_documents(
        self,
        folder_path: str,
        collection_name: str,
    ) -> PGVector:
        """Load documents into vectorstore."""
        text_documents = self._load_docs(folder_path)

        logger.info(f"Loading {text_documents} text-documents into vectorstore")
        text_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        texts = text_splitter.split_documents(text_documents)

        json_path = os.path.join(
            path_extraction_folder, f"{collection_name}_split_texts.json"
        )
        with open(json_path, "w") as json_file:
            # Use jsonable_encoder to ensure the data is serializable
            json.dump(jsonable_encoder(texts), json_file, indent=4)

        # Add metadata for separate filtering
        for text in texts:
            text.metadata["type"] = "Text"

        docs = [*texts]

        logger.info(f"Loading {len(texts)} text-documents into vectorstore")

        return PGVector.from_documents(
            embedding=self.embedding_model,
            documents=docs,
            collection_name=collection_name,
            connection_string=self.connection_str,
            pre_delete_collection=True,
        )

    def _load_docs(
        self,
        dir_path: str,
    ) -> List[Document]:
        """
        Using specified PDF miner to convert PDF documents to raw text chunks.

        Fallback: PyPDF
        """
        documents = []
        for file_name in os.listdir(dir_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            # Load PDF files
            if file_extension == ".pdf":
                logger.info(f"Loading {file_name} into vectorstore")
                file_path = f"{dir_path}/{file_name}"
                try:
                    loader: Any = self.pdf_loader(file_path)  # type: ignore
                    file_docs = loader.load()
                    documents.extend(file_docs)

                    logger.info(f"{file_docs}")

                    # Serialize using jsonable_encoder and save to JSON
                    json_path = os.path.join(
                        path_extraction_folder, os.path.splitext(file_name)[0] + ".json"
                    )
                    with open(json_path, "w") as json_file:
                        json.dump(jsonable_encoder(file_docs), json_file, indent=4)
                    logger.info(
                        f"{file_name} loaded and saved in JSON format successfully"
                    )
                except Exception as e:
                    logger.error(
                        f"Could not extract text from PDF {file_name}: {repr(e)}"
                    )

        return documents


if __name__ == "__main__":

    asyncio.run(init_db())

    create_super_user()

    # logger.info("Starting PDF extraction pipeline")
    # pipeline = PDFExtractionPipeline()
    # pipeline.run(collection_name)
