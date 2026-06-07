import logging
from chromadb import PersistentClient
from app.core.config import VECTOR_DB_DIR, settings

logger = logging.getLogger(__name__)

class VectorStoreService:

    def __init__(self) -> None:
        self.client = PersistentClient(path=str(VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )
    
    def add_chunks(
        self,
        file_id: str,
        chunks: list[dict]
    ) -> None:
        
        if not chunks:
            logger.warning("No chunks provided to save in Vector Store.")
            return

        self.collection.add(
            
            ids=[
                f"{file_id}_chunk_{chunk['chunk_id']}"
                for chunk in chunks
            ],
            documents=[
                chunk["text"]
                for chunk in chunks
            ],
            embeddings=[
                chunk["embedding"]
                for chunk in chunks
            ],
            
            metadatas=[
                {
                    "file_id": file_id,
                    "page": chunk["page"],
                    "tokens_count": chunk["tokens_count"],
                }
                for chunk in chunks
            ],
        )
        logger.info(f"Successfully stored {len(chunks)} chunks for file_id: {file_id}")