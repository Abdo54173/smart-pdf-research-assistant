from pydantic import BaseModel

class ChatRequest(BaseModel):
    file_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]