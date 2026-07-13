from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)
    document_ids: list[str]
    question: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]