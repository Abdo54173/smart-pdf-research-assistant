from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.document import Document

class DocumentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, document: Document) -> Document:
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def get_by_id(self, document_id: str) -> Document | None:
        statement = select(Document).where(Document.id == document_id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def get_all(self) -> list[Document]:
        statement = select(Document).order_by(Document.created_at.desc())
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def delete(self, document: Document) -> None:
        await self.db.delete(document) 
        await self.db.commit()