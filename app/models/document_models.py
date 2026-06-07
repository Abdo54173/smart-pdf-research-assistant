from pydantic import BaseModel

class EmbeddedChunk(BaseModel):
    chunk_id: int
    page: int
    text: str
    tokens_count: int
    embedding: list[float]

class ProcessedDocument(BaseModel):
    total_pages: int
    total_chunks: int
    chunks: list[dict]