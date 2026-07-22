from pydantic import BaseModel

class UploadResponse(BaseModel):
    document_id: str
    conversation_id: str
    original_filename: str
    stored_filename: str
    message: str