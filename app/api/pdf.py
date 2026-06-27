from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import (
    get_document_processing_service,
    get_pdf_service,
    get_vector_store_service,
)
from app.core.config import UPLOAD_DIR
from app.models.pdf_models import UploadResponse
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.services.pdf_service import PDFService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"],
)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
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
):
    content =await file.read()

    pdf_service.validate_pdf(
        filename=file.filename,
        content=content,
    )

    stored_filename = pdf_service.save_pdf(
        filename=file.filename,
        content=content,
    )

    file_path = Path(UPLOAD_DIR / stored_filename)

    processed_document = (
        document_processing_service.process_document(
            file_path=file_path,
        )
    )

    vector_store_service.add_chunks(
        file_id=stored_filename,
        chunks=processed_document.chunks,
    )

    return UploadResponse(
        original_filename=file.filename,
        stored_filename=stored_filename,
        message="PDF uploaded and indexed successfully",
    )
