from uuid import UUID

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    repository_id: UUID


class CreateSessionResponse(BaseModel):
    session_id: UUID


class ChatMessageRequest(BaseModel):
    session_id: UUID
    question: str


class ChatMessageResponse(BaseModel):
    answer: str
    history_count: int