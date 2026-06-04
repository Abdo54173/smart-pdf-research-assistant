from pathlib import Path

from app.models.document_models import ProcessedDocument
from app.services.chunking_service import ChunkingService
from app.services.pdf_parser_service import PDFParserService

class DocumentProcessingService:

    def __init__(
        self,
        pdf_parser_service: PDFParserService,
        chunking_service: ChunkingService,
    ) -> None:
        self.pdf_parser_service = pdf_parser_service
        self.chunking_service = chunking_service

    def process_document(
            self,
            file_path: Path,
    ) -> ProcessedDocument:
        
        pages = self.pdf_parser_service.extract_pages(file_path)

        chunks = self.chunking_service.chunk_pages(pages)

        return ProcessedDocument(
            total_pages=len(pages),
            total_chunks=len(chunks),
            chunks=chunks,
        )