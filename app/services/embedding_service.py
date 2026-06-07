import logging
from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:

    def __init__(
        self,
        model_name: str = settings.EMBEDDING_MODEL_NAME,
    ) -> None:
        
        logger.info(f"Loading embedding model: {model_name}")

        try:
            self.model = SentenceTransformer(model_name)
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model {model_name}: {e}")
            raise RuntimeError(f"Could not initialize EmbeddingService: {e}")

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Cannot embed empty or whitespace-only text.")
        
        return self.model.encode(text, convert_to_numpy=True,).tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return [emb.tolist() for emb in embeddings]