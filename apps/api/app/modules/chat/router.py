from uuid import UUID

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.chat.schemas import(
    CreateSessionRequest, 
    CreateSessionResponse, 
    ChatMessageRequest, 
    ChatMessageResponse, 
    ChatSessionItem, 
    ChatSessionListResponse, 
    ChatMessagesResponse, 
    ChatMessageItem,
    RenameChatRequest,
    RenameChatResponse,
    )

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

    return StreamingResponse(
        ChatService.send_message(
            db=db,
            session_id=request.session_id,
            question=request.question,
        ),
        media_type="text/event-stream",
    )

@router.get("/sessions")
async def list_sessions(

    repository_id: UUID,

    db: AsyncSession = Depends(get_db),

):

    sessions = await ChatService.list_sessions(
        db=db,
        repository_id=repository_id,
    )

    return {
        "sessions": sessions
    }

@router.get(
    "/{session_id}/messages",
    response_model=ChatMessagesResponse,
)
async def get_session_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    messages = await ChatService.get_session_messages(
        db=db,
        session_id=session_id,
    )

    return ChatMessagesResponse(

        messages=[

            ChatMessageItem.model_validate(message)

            for message in messages

        ]

    )

@router.patch(
    "/{session_id}/title",
    response_model=RenameChatResponse,
)
async def rename_chat(
    session_id: UUID,
    request: RenameChatRequest,
    db: AsyncSession = Depends(get_db),
):

    result = await ChatService.rename_chat(
        db=db,
        session_id=session_id,
        title=request.title,
    )

    return RenameChatResponse(
        success=result["success"],
    )

@router.delete(
    "/repository/{repository_id}",
)
async def delete_repository_chats(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await ChatService.delete_all_sessions(
        db=db,
        repository_id=repository_id,
    )

    return {
        "success": True,
    }

@router.delete(
    "/{session_id}",
)
async def delete_chat(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    await ChatService.delete_session(
        db=db,
        session_id=session_id,
    )

    return {
        "success": True,
    }