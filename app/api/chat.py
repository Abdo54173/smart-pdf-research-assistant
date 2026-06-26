from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_chat_service
from app.models.chat_models import (
    ChatRequest,
    ChatResponse,
)
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
) -> ChatResponse:
    
    try:
        result = chat_service.ask(
            file_id=request.file_id,
            question=request.question,
        )

        return ChatResponse(**result)
    
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )