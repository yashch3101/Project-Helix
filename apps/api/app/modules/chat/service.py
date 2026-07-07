from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.repository import ChatRepository
# from app.modules.context.service import ContextService
from app.modules.ai.service import AIService
from app.modules.chat.history import HistoryBuilder
from app.modules.chat.query_rewriter import QueryRewriter


class ChatService:

    @staticmethod
    async def create_session(
        db: AsyncSession,
        repository_id,
    ):

        return await ChatRepository.create_session(
            db=db,
            repository_id=repository_id,
        )

    @staticmethod
    async def send_message(
        db: AsyncSession,
        session_id,
        question: str,
    ):

        # 1. Load chat session
        session = await ChatRepository.get_session(
            db=db,
            session_id=session_id,
        )

        if session is None:
            raise Exception("Chat session not found")

        # 2. Load previous conversation
        history = await ChatRepository.get_messages(
            db=db,
            session_id=session_id,
        )

        conversation_history = HistoryBuilder.build(
            history
        )

        search_query = await QueryRewriter.rewrite(
            history=conversation_history,
            question=question,
        )

        print("=" * 80)
        print("ORIGINAL QUESTION:")
        print(question)

        print("-" * 80)

        print("SEARCH QUERY:")
        print(search_query)

        print("=" * 80)

        # 3. Build repository context
        # context = await ContextService.build(
        #     db=db,
        #     repository_id=session.repository_id,
        #     query=question,
        # )

        # 4. Ask AI
        answer = await AIService.ask(
            db=db,
            repository_id=session.repository_id,
            question=question,
            history=conversation_history,
            search_query=search_query,
        )

        # 5. Save user message
        await ChatRepository.save_message(
            db=db,
            session_id=session.id,
            role="user",
            content=question,
        )

        # 6. Save assistant reply
        await ChatRepository.save_message(
            db=db,
            session_id=session.id,
            role="assistant",
            content=answer,
        )

        return {
            "answer": answer,
            "history_count": len(history),
        }