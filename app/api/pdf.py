from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import (
    get_document_processing_service,
    get_document_service,
    get_pdf_service,
    get_vector_store_service,
    get_conversation_service,
)
from app.core.config import UPLOAD_DIR
from app.models.pdf_models import UploadResponse
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_service import DocumentService
from app.services.pdf_service import PDFService
from app.services.vector_store_service import VectorStoreService
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    document_service: Annotated[
        DocumentService,
        Depends(get_document_service),
    ] = None,
    pdf_service: Annotated[
        PDFService,
        Depends(get_pdf_service),
    ] = None,
    document_processing_service: Annotated[
        DocumentProcessingService,
        Depends(get_document_processing_service),
    ] = None,
    vector_store_service: Annotated[
        VectorStoreService,
        Depends(get_vector_store_service),
    ] = None,
    conversation_service: Annotated[
        ConversationService,
        Depends(get_conversation_service),
    ] = None,
):
    content =await file.read()

    try:
        pdf_service.validate_pdf(
            filename=file.filename,
            content=content,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    stored_filename = pdf_service.save_pdf(
        filename=file.filename,
        content=content,
    )

    file_path = Path(UPLOAD_DIR / stored_filename)

    document = None
    conversation = None

    try:
        document = await document_service.create_document(
            filename=file.filename,
            file_path=str(file_path),
        )
        conversation = await conversation_service.create_conversation(
            title=Path(file.filename).stem,
            document_ids=[str(document.id)],
        )

        processed_document = document_processing_service.process_document(
                file_path=file_path,
            )

        await vector_store_service.add_chunks(
            document_id=str(document.id),
            document_name=document.filename,
            chunks=processed_document.chunks,
        )

    except Exception as e:

        if document is not None:
            await document_service.delete_document(document.id)

        pdf_service.delete_pdf(stored_filename)

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return UploadResponse(
        document_id=document.id,
        conversation_id=conversation.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        message="PDF uploaded and indexed successfully",
    )
