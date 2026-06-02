from app.services.pdf_service import PDFService


def get_pdf_service() -> PDFService:
    return PDFService()