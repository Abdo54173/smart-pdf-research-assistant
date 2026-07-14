from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    title: str
    document_ids: list[str]


class CreateConversationResponse(BaseModel):
    conversation_id: str
    title: str