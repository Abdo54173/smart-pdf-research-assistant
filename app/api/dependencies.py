from app.services.chat_service import ChatService
from app.services.chunking_service import ChunkingService
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.services.pdf_parser_service import PDFParserService
from app.services.retriever_service import RetrieverService
from app.services.vector_store_service import VectorStoreService

embedding_service = EmbeddingService()
pdf_parser_service = PDFParserService()
chunking_service = ChunkingService()
vector_store_service = VectorStoreService()

document_processing_service = DocumentProcessingService(
    pdf_parser_service=pdf_parser_service,
    chunking_service=chunking_service,
    embedding_service=embedding_service,
)

retriever_service = RetrieverService(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service,
)

chat_service = ChatService(
    retriever_service=retriever_service,
)

def get_pdf_service() -> PDFService:
    return PDFService()


def get_document_processing_service() -> DocumentProcessingService:
    return document_processing_service


def get_vector_store_service() -> VectorStoreService:
    return vector_store_service


def get_chat_service() -> ChatService:
    return chat_service