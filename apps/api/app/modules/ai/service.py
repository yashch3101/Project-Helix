import google.generativeai as genai  # type: ignore[import]

from app.core.config import settings
# from app.modules.ai.prompt import SYSTEM_PROMPT
from app.modules.retrieval.service import RetrievalService
from app.modules.ai.prompt_builder import PromptBuilder

genai.configure(
    api_key=settings.gemini_api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class AIService:

    @staticmethod
    async def ask(
        db,
        repository_id,
        question: str,
        history: str = "",
        search_query: str = "",
    ):

        retrieval = await RetrievalService.search(
            db=db,
            repository_id=repository_id,
            query=search_query,
            top_k=10,
        )

        # Build repository context

        context = ""

        for item in retrieval:

            context += f"""
            FILE:
            {item["chunk_name"]}

            TYPE:
            {item["chunk_type"]}

            LINES:
            {item["start_line"]} - {item["end_line"]}

            CONTENT:
            {item["content"]}

            ------------------------------------
            """

        # Build final prompt

        prompt = PromptBuilder.build(
            history=history,
            context=context,
            question=question,
        )

        response = model.generate_content(
            prompt
        )

        return response.text