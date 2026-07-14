from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class CreateSessionRequest(BaseModel):
    repository_id: UUID


class CreateSessionResponse(BaseModel):
    session_id: UUID


class ChatMessageRequest(BaseModel):
    session_id: UUID
    question: str

class Citation(BaseModel):
    file: str
    type: str
    start_line: int
    end_line: int
    score: float

class ChatMessageResponse(BaseModel):
    answer: str
    history_count: int
    citations: list[Citation]

class ChatSessionItem(BaseModel):

    id: UUID
    title: str | None = None
    updated_at: datetime

class ChatSessionListResponse(BaseModel):

    sessions: list[ChatSessionItem]

class ChatMessageItem(BaseModel):

    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
        
class ChatMessagesResponse(BaseModel):

    messages: list[ChatMessageItem]

class RenameChatRequest(BaseModel):

    title: str

class RenameChatResponse(BaseModel):

    success: bool