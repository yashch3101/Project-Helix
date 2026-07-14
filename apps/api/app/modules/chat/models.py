import uuid

from sqlalchemy import Column, ForeignKey, Text, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_model import BaseModel


class ChatSession(BaseModel):

    __tablename__ = "chat_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_id = Column(
        UUID(as_uuid=True),
        ForeignKey("repositories.id"),
        nullable=False,
    )

    title = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete",
    )

class ChatMessage(BaseModel):

    __tablename__ = "chat_messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id"),
        nullable=False,
    )

    role = Column(Text)

    content = Column(Text)

    session = relationship(
        "ChatSession",
        back_populates="messages",
    )