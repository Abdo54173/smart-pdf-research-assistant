from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.services.pdf_service import PDFService
from app.services.pdf_parser_service import PDFParserService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.document_processing_service import DocumentProcessingService

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_document_repository(
    db: AsyncSession,
) -> DocumentRepository:
    return DocumentRepository(db)

def get_document_service(
    document_repository: DocumentRepository,
) -> DocumentService:
    return DocumentService(document_repository)

def get_document_processing_service() -> DocumentProcessingService:
    return DocumentProcessingService(
        pdf_parser_service=PDFParserService(),
        chunking_service=ChunkingService(),
        embedding_service=EmbeddingService(),
        vector_store_service=VectorStoreService(),
    )

def get_pdf_service() -> PDFService:
    return PDFService()