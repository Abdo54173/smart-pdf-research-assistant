from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

class RetrieverService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
    ) -> None:

        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    def retrieve(
        self,
        file_id: str,
        query: str,
        top_k: int = 5,
    ) -> dict:

        query_embedding = self.embedding_service.embed_text(
            query
        )

        return self.vector_store_service.search(
            file_id=file_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )