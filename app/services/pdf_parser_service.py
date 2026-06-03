import logging
from pathlib import Path
import re
from pypdf import PdfReader

logger = logging.getLogger(__name__)

class PDFParserService:

    def extract_pages(self, file_path: Path) -> list[dict]:

        if not file_path.exists():
            logger.error(f"Internal Error: File does not exist at path Safely-Hidden -> {file_path}")
            raise FileNotFoundError("The requested PDF file could not be found.")
        
        try:    
            reader = PdfReader(file_path)
            pages = []

            for page_number, page in enumerate(reader.pages, start=1):
                raw_text = page.extract_text() or ""
                cleaned_text = re.sub(r'\n+', '\n', raw_text).strip()

                pages.append(
                    {
                        "page": page_number,
                        "text": cleaned_text,
                    }
                )
        
            return pages
        
        except Exception as e:
            logger.exception(f"Failed to parse PDF file. Internal error: {str(e)}")
            raise RuntimeError("An error occurred while processing the PDF file structure.")