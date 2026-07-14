from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_conversation_service
from app.models.conversation_models import (
    CreateConversationRequest,
    CreateConversationResponse,
)
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=CreateConversationResponse,
)
async def create_conversation(
    request: CreateConversationRequest,
    conversation_service: Annotated[
        ConversationService,
        Depends(get_conversation_service),
    ],
):
    conversation = await conversation_service.create_conversation(
        title=request.title,
        document_ids=request.document_ids,
    )

    return CreateConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
    )