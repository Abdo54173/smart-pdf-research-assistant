from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_chat_service
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/ask",
    response_model=ChatResponse,
)
async def ask_question(
    request: ChatRequest,
    chat_service: Annotated[
        ChatService,
        Depends(get_chat_service),
    ],
):
    try:
        result = await chat_service.ask(
            conversation_id=request.conversation_id,
            question=request.question,
        )

        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )