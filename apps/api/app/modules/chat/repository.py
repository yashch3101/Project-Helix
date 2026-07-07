from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.models import ChatSession, ChatMessage


class ChatRepository:

    @staticmethod
    async def create_session(
        db: AsyncSession,
        repository_id,
    ):

        session = ChatSession(
            repository_id=repository_id,
        )

        db.add(session)

        await db.commit()

        await db.refresh(session)

        return session


    @staticmethod
    async def get_session(
        db: AsyncSession,
        session_id,
    ):

        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id
            )
        )

        return result.scalar_one_or_none()


    @staticmethod
    async def save_message(
        db: AsyncSession,
        session_id,
        role,
        content,
    ):

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )

        db.add(message)

        await db.commit()

        await db.refresh(message)

        return message


    @staticmethod
    async def get_messages(
        db: AsyncSession,
        session_id,
    ):

        result = await db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
        )

        return result.scalars().all()