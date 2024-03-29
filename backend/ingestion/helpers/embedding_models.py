# -*- coding: utf-8 -*-
# mypy: disable-error-code="call-arg"
# TODO: Change langchain param names to match the new langchain version

import logging
from typing import List, Optional, Union

from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

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
        vectors: List[Union[List[float], None]] = self.document_embedding_store.mget([text])
        text_embeddings = vectors[0]

        if text_embeddings is None:
            text_embeddings = self.underlying_embeddings.embed_query(text)
            self.document_embedding_store.mset(list(zip([text], [text_embeddings])))

        return text_embeddings


def get_embedding_model(emb_model: Optional[str]) -> CacheBackedEmbeddings:
    """
    Get the embedding model from the embedding model type.
    """
    underlying_embeddings = OpenAIEmbeddings()

    embedder = CacheBackedEmbeddingsExtended(underlying_embeddings)

    # store = get_redis_store()
    # embedder = CacheBackedEmbeddingsExtended.from_bytes_store(
    #     underlying_embeddings, store, namespace=underlying_embeddings.model
    # )
    return embedder
