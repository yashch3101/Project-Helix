from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.chat.schemas import CreateSessionRequest, CreateSessionResponse, ChatMessageRequest, ChatMessageResponse
from app.modules.chat.service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/session",
    response_model=CreateSessionResponse,
)
async def create_session(
    payload: CreateSessionRequest,
    db: AsyncSession = Depends(get_db),
):

    session = await ChatService.create_session(
        db=db,
        repository_id=payload.repository_id,
    )

    return CreateSessionResponse(
        session_id=session.id,
    )

@router.post(
    "/message",
    response_model=ChatMessageResponse,
)
async def send_message(
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
):

    result = await ChatService.send_message(
        db=db,
        session_id=request.session_id,
        question=request.question,
    )

    return ChatMessageResponse(
        answer=result["answer"],
        history_count=result["history_count"],
    )