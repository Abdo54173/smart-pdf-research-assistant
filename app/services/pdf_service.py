from pathlib import Path
from uuid import uuid4

from app.core.config import UPLOAD_DIR


class PDFService:
    MAX_FILE_SIZE_MB = 10

    def validate_pdf(
        self,
        filename: str | None,
        content: bytes,
    ) -> None:

        if not filename:
            raise ValueError("Filename is required")

        if not filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed")

        if len(content) > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(
                f"Maximum file size is {self.MAX_FILE_SIZE_MB} MB"
            )

    def generate_unique_filename(
        self,
        filename: str,
    ) -> str:
        return f"{uuid4()}-{filename}"

    def save_pdf(
        self,
        filename: str,
        content: bytes,
    ) -> str:

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        unique_filename = self.generate_unique_filename(filename)

        file_path = UPLOAD_DIR / unique_filename

        with open(file_path, "wb") as file:
            file.write(content)

        return unique_filename