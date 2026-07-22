import logging

from app.entities.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository

logger = logging.getLogger(__name__)

class VectorStoreService:

    def __init__(
        self,
        document_chunk_repository: DocumentChunkRepository,
    ) -> None:
        self.document_chunk_repository = document_chunk_repository
    
    async def add_chunks(
        self,
        document_id: str,
        document_name: str,
        chunks: list[dict],
    ) -> None:

        if not chunks:
            logger.warning("No chunks provided to save in Vector Store.")
            return

        document_chunks = []

        for chunk in chunks:

            document_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk["chunk_id"],
                document_name=document_name,
                page_number=chunk["page"],
                content=chunk["text"],
                embedding=chunk["embedding"],
            )

            document_chunks.append(document_chunk)

        await self.document_chunk_repository.create_many(
            document_chunks
        )

        logger.info(
            f"Successfully stored {len(chunks)} chunks for document_id: {document_id}"
        )

    async def search(
        self,
        document_ids: list[str],
        query_embedding: list[float],
        top_k: int = 5,
    ):

        results = []

        for document_id in document_ids:
            chunks = await self.document_chunk_repository.search(
                document_id=document_id,
                query_embedding=query_embedding,
                top_k=top_k,
            )
            results.extend(chunks)

        results.sort(key=lambda x: x["distance"])

        return results[:top_k]
    