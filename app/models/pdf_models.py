from pydantic import BaseModel

class UploadResponse(BaseModel):
    original_filename: str
    stored_filename: str
    message: str