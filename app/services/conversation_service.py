from uuid import uuid4

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

class ConversationService:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    async def create_conversation(
        self,
        title: str,
    ) -> Conversation:
        clean_title = title.strip() if title else "New Conversation"

        conversation = Conversation(
            id=str(uuid4()),
            title=clean_title,
        )

        return await self.conversation_repository.create(conversation)
    
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