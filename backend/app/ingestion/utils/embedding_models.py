from typing import List, Optional, Union

from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import OpenAIEmbeddings
from backend.app.init_db import logger


class CacheBackedEmbeddingsExtended(CacheBackedEmbeddings):
    def embed_query(self, text: str) -> List[float]:
        """
        Embed query text.

        Extended to support caching

        Args:
            text: The text to embed.

        Returns:
            The embedding for the given text.
        """
        vectors: List[Union[List[float], None]] = self.document_embedding_store.mget(
            [text]
        )
        text_embeddings = vectors[0]

        if text_embeddings is None:
            text_embeddings = self.underlying_embeddings.embed_query(text)
            self.document_embedding_store.mset(list(zip([text], [text_embeddings])))

        return text_embeddings


def get_embedding_model() -> CacheBackedEmbeddings:
    """
    Get the embedding model from the embedding model type.
    """

    underlying_embeddings = OpenAIEmbeddings()

    # embedder = CacheBackedEmbeddingsExtended(underlying_embeddings)

    logger.info(f"Loaded embedding model: {underlying_embeddings.model}")

    # store = get_redis_store()
    # embedder = CacheBackedEmbeddingsExtended.from_bytes_store(
    #     underlying_embeddings, store, namespace=underlying_embeddings.model
    # )
    return underlying_embeddings
