from pydantic import BaseModel


class ProcessedDocument(BaseModel):
    total_pages: int
    total_chunks: int
    chunks: list[dict]