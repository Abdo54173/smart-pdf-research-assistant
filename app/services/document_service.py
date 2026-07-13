from app.entities.document import Document
from app.repositories.document_repository import DocumentRepository

class DocumentService:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def create_document(
        self,
        filename: str,
        file_path: str,
    ) -> Document:
        
        if not filename.strip():
            raise ValueError("Filename cannot be empty.")
        
        document = Document(
            filename=filename,
            file_path=file_path,
        )

        return await self.document_repository.create(document)
    
    async def get_document(
        self,
        document_id: str,
    ) -> Document | None:
        return await self.document_repository.get_by_id(document_id)
    
    async def get_documents(self) -> list[Document]:
        return await self.document_repository.get_all()
    
    async def delete_document(self, document_id: str) -> bool:
        
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            return False
            
        await self.document_repository.delete(document)
        return True