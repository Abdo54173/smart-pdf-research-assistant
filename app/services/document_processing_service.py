from pathlib import Path

from app.models.document_models import ProcessedDocument
from app.services.chunking_service import ChunkingService
from app.services.pdf_parser_service import PDFParserService
from app.services.embedding_service import EmbeddingService

class DocumentProcessingService:

    def __init__(
        self,
        pdf_parser_service: PDFParserService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
    ) -> None:
        self.pdf_parser_service = pdf_parser_service
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service

    def process_document(
            self,
            file_path: Path,
    ) -> ProcessedDocument:
        
        pages = self.pdf_parser_service.extract_pages(file_path)

        chunks = self.chunking_service.chunk_pages(pages)

        if not chunks:
            return ProcessedDocument(total_pages=len(pages), total_chunks=0, chunks=[])

        texts_to_embed = [chunk["text"] for chunk in chunks]

        all_embeddings = self.embedding_service.embed_texts(texts_to_embed)

        embedded_chunks = []
        
        for chunk, embedding in zip(chunks, all_embeddings):
            embedded_chunks.append(
                {
                    **chunk,
                    "embedding": embedding,
                }
            )

        return ProcessedDocument(
            total_pages=len(pages),
            total_chunks=len(chunks),
            chunks=embedded_chunks,
        )