from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import get_pdf_service
from app.models.pdf_models import UploadResponse
from app.services.pdf_service import PDFService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    pdf_service: Annotated[PDFService, Depends(get_pdf_service)] = None,
):
    content =await file.read()

    pdf_service.validate_pdf(
        filename=file.filename,
        content=content,
    )

    filename =pdf_service.save_pdf(
        filename=file.filename,
        content=content,
    )

    return UploadResponse(
        filename=filename,
        message="PDF uploaded successfully"
    )