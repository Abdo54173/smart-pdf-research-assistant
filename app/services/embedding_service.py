import logging

import cohere

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:

    def __init__(self) -> None:

        try:
            self.client = cohere.Client(
                api_key=settings.COHERE_API_KEY
            )

            self.model_name = settings.EMBEDDING_MODEL_NAME

            logger.info(
                f"Cohere embedding model loaded: {self.model_name}"
            )

        except Exception as e:
            logger.error(
                f"Failed to initialize Cohere client: {e}"
            )

            raise RuntimeError(
                f"Could not initialize EmbeddingService: {e}"
            )

    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError(
                "Cannot embed empty text."
            )

        response = self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type="search_query",
        )

        return response.embeddings[0]

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = self.client.embed(
            texts=texts,
            model=self.model_name,
            input_type="search_document",
        )

        return response.embeddings