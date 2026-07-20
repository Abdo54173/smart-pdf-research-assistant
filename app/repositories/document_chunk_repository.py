from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.document_chunk import DocumentChunk

class DocumentChunkRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
        self.db.add(chunk)
        await self.db.flush()
        await self.db.refresh(chunk)
        return chunk
    
    async def create_many(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        self.db.add_all(chunks)
        await self.db.flush()

    async def get_by_document_id(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:
        result = await self.db.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
        )
        return list(result.scalars().all())
    
    async def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int,
    ) -> list[dict]:

        result = await self.db.execute(
            select(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                ).label("distance"),
            )
            .where(
                DocumentChunk.document_id == document_id
            )
            .order_by("distance")
            .limit(top_k)
        )
    
        return [
            {
                "text": chunk.content,
                "metadata": {
                    "document_id": chunk.document_id,
                    "page": chunk.page_number,
                },
                "distance": distance,
            }
            for chunk, distance in result.all()
        ]
    
    async def delete_by_document_id(
        self,
        document_id: UUID,
    ) -> None:
        await self.db.execute(
            delete(DocumentChunk).where(
                DocumentChunk.document_id == document_id
            )
        )
        await self.db.flush()