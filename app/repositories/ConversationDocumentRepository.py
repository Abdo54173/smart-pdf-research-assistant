from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.conversation_document import ConversationDocument

class ConversationDocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_documents(
        self,
        conversation_id: str,
        document_ids: list[str],
    ) -> None:
        
        unique_doc_ids = set(document_ids)
        if not unique_doc_ids:
            return
        
        existing_statement = select(ConversationDocument.document_id).where(
            ConversationDocument.conversation_id == conversation_id,
            ConversationDocument.document_id.in_(unique_doc_ids)
        )
        existing_result = await self.db.execute(existing_statement)
        existing_ids = set(existing_result.scalars().all())

        new_doc_ids = unique_doc_ids - existing_ids
        if not new_doc_ids:
            return

        links = [
            ConversationDocument(
                conversation_id=conversation_id,
                document_id=document_id,
            )
            for document_id in new_doc_ids
        ]

        try:
            self.db.add_all(links)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback() 
            raise RuntimeError(f"Database error while linking documents: {e}")

    async def get_document_ids(
        self,
        conversation_id: str,
    ) -> list[str]:

        result = await self.db.execute(
            select(ConversationDocument.document_id).where(
                ConversationDocument.conversation_id == conversation_id
            )
        )

        return list(result.scalars().all())