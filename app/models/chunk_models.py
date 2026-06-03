from pydantic import BaseModel


class ChunkData(BaseModel):
    page: int
    chunk_id: int
    text: str