from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.repository import ChatRepository
# from app.modules.context.service import ContextService
from app.modules.ai.service import AIService
from app.modules.chat.history import HistoryBuilder
from app.modules.chat.query_rewriter import QueryRewriter
from app.modules.chat.events import ChatEvent
from app.modules.chat.citations import CitationBuilder
from app.modules.chat.title_service import TitleService


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

        is_first_message = len(history) == 0

        conversation_history = HistoryBuilder.build(
            history
        )

        search_query = await QueryRewriter.rewrite(
            history=conversation_history,
            question=question,
        )

        if is_first_message:

            title = await TitleService.generate(
                question
            )

            await ChatRepository.update_title(
                db=db,
                session=session,
                title=title,
            )

            print("=" * 80)
            print("CHAT TITLE:")
            print(title)
            print("=" * 80)

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
        

        # 4. Save user message

        await ChatRepository.save_message(
            db=db,
            session_id=session.id,
            role="user",
            content=question,
        )

        assistant_answer = ""

        retrieval = []

        reasoning = None

        print("=" * 80)
        print("CHAT SESSION REPOSITORY ID")
        print(session.repository_id)
        print(type(session.repository_id))
        print("=" * 80)

        async for event in AIService.ask(
            db=db,
            repository_id=session.repository_id,
            question=question,
            history=conversation_history,
            search_query=search_query,
        ):

            if event["type"] == "reasoning":

                reasoning = event["data"]

                retrieval = reasoning["retrieval"]

                yield ChatEvent.reasoning(
                    {
                        "trace": reasoning["trace"]
                    }
                )

                yield ChatEvent.evidence(
                    reasoning["evidence"]
                )

                yield ChatEvent.impact(
                    reasoning["impact"]
                )

                continue

            if event["type"] == "token":

                token = event["data"]

                assistant_answer += token

                yield ChatEvent.token(token)

        citations = CitationBuilder.build(
            retrieval
        )

        yield ChatEvent.citations(
            citations
        )

        # 5. Save assistant reply after streaming completes

        await ChatRepository.save_message(
            db=db,
            session_id=session.id,
            role="assistant",
            content=assistant_answer,
        )

        yield ChatEvent.done()

    @staticmethod
    async def list_sessions(
        db,
        repository_id,
    ):

        return await ChatRepository.list_sessions(
            db=db,
            repository_id=repository_id,
        )

    @staticmethod
    async def get_session_messages(
        db: AsyncSession,
        session_id,
    ):

        session = await ChatRepository.get_session(
            db=db,
            session_id=session_id,
        )

        if session is None:
            raise Exception("Chat session not found")

        messages = await ChatRepository.get_session_messages(
            db=db,
            session_id=session_id,
        )

        return messages

    @staticmethod
    async def rename_chat(
        db: AsyncSession,
        session_id,
        title: str,
    ):

        session = await ChatRepository.get_session(
            db=db,
            session_id=session_id,
        )

        if session is None:
            raise Exception("Chat session not found")

        await ChatRepository.update_title(
            db=db,
            session=session,
            title=title,
        )

        return {
            "success": True,
        }

    @staticmethod
    async def delete_all_sessions(
        db: AsyncSession,
        repository_id,
    ):
        await ChatRepository.delete_all_sessions(
            db=db,
            repository_id=repository_id,
        )

        return True

    @staticmethod
    async def delete_session(
        db: AsyncSession,
        session_id,
    ):

        session = await ChatRepository.get_session(
            db=db,
            session_id=session_id,
        )

        if session is None:
            raise Exception("Chat session not found")

        await ChatRepository.delete_session(
            db=db,
            session_id=session_id,
        )

        return True