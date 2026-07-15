from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    document_ids: list[str] | None = None
    question: str


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sources: list[dict]