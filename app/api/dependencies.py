from app.services.pdf_service import PDFService
from app.services.chat_service import ChatService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.retriever_service import RetrieverService
from app.services.vector_store_service import VectorStoreService

def get_pdf_service() -> PDFService:
    return PDFService()

def get_chat_service() -> ChatService:

    embedding_service = EmbeddingService()

    vector_store_service = VectorStoreService()

    retriever_service = RetrieverService(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

    return ChatService(
        retriever_service=retriever_service,
    )