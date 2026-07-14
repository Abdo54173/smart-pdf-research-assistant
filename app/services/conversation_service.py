from uuid import uuid4

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.ConversationDocumentRepository import ConversationDocumentRepository
from app.repositories.message_repository import MessageRepository

class ConversationService:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        conversation_document_repository: ConversationDocumentRepository
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.conversation_document_repository = conversation_document_repository

    async def create_conversation(
        self,
        title: str,
        document_ids: list[str],
    ) -> Conversation:
        clean_title = title.strip() if title else "New Conversation"

        conversation = Conversation(
            id=str(uuid4()),
            title=clean_title,
        )

        conversation = await self.conversation_repository.create(conversation)

        await self.attach_documents(
        conversation.id,
        document_ids,
    )

        return conversation
    
    async def get_conversation(
        self,
        conversation_id: str,
    ) -> Conversation | None:
        return await self.conversation_repository.get_by_id(
            conversation_id
        )
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> Message:
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")
        
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        return await self.message_repository.create(message)
    
    async def get_history(
        self,
        conversation_id: str,
    ) -> list[Message]:
        
        conversation = await self.conversation_repository.get_by_id(conversation_id)
        if not conversation:
            return []
        
        return await self.message_repository.get_last_messages(
            conversation_id
        )
    
    async def attach_documents(
        self,
        conversation_id: str,
        document_ids: list[str],
    ) -> None:
        await self.conversation_document_repository.add_documents(
            conversation_id,
            document_ids,
        )
    
    async def get_document_ids(
        self,
        conversation_id: str,
    ) -> list[str]:
        return await self.conversation_document_repository.get_document_ids(
            conversation_id
        )