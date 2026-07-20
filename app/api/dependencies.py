from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal

from app.repositories.document_repository import DocumentRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.ConversationDocumentRepository import ConversationDocumentRepository
from app.repositories.document_chunk_repository import DocumentChunkRepository

from app.services.document_service import DocumentService
from app.services.conversation_service import ConversationService
from app.services.pdf_service import PDFService
from app.services.pdf_parser_service import PDFParserService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.services.retriever_service import RetrieverService
from app.services.chat_service import ChatService

from app.llms.base import BaseLLM
from app.llms.factory import LLMFactory


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Singleton Services

pdf_service = PDFService()
pdf_parser_service = PDFParserService()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store_service = VectorStoreService()
llm = LLMFactory.create()

def get_document_chunk_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> DocumentChunkRepository:
    return DocumentChunkRepository(db)

def get_document_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DocumentService:
    return DocumentService(
        document_repository=DocumentRepository(db),
    )


def get_conversation_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ConversationService:
    return ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
        conversation_document_repository=ConversationDocumentRepository(db),
    )


def get_pdf_service() -> PDFService:
    return pdf_service


def get_embedding_service() -> EmbeddingService:
    return embedding_service


def get_vector_store_service(
    document_chunk_repository: Annotated[
        DocumentChunkRepository,
        Depends(get_document_chunk_repository),
    ],
) -> VectorStoreService:
    return VectorStoreService(
        document_chunk_repository=document_chunk_repository,
    )


def get_document_processing_service() -> DocumentProcessingService:
    return DocumentProcessingService(
        pdf_parser_service=pdf_parser_service,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
    )


def get_retriever_service(
    embedding_service: Annotated[
        EmbeddingService,
        Depends(get_embedding_service),
    ],
    vector_store_service: Annotated[
        VectorStoreService,
        Depends(get_vector_store_service),
    ],
) -> RetrieverService:
    return RetrieverService(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

def get_llm() -> BaseLLM:
    return llm

def get_chat_service(
    retriever_service: Annotated[
        RetrieverService,
        Depends(get_retriever_service),
    ],
    conversation_service: Annotated[
        ConversationService,
        Depends(get_conversation_service),
    ],
    llm: Annotated[
        BaseLLM,
        Depends(get_llm),
    ],
) -> ChatService:
    return ChatService(
        retriever_service=retriever_service,
        conversation_service=conversation_service,
        llm=llm,
    )