import google.generativeai as genai  # type: ignore[import]

from app.core.config import settings
# from app.modules.ai.prompt import SYSTEM_PROMPT
from app.modules.reasoning.service import ReasoningService
from app.modules.ai.reasoning_formatter import ReasoningFormatter
from app.modules.ai.reasoning_prompt import SYSTEM_PROMPT
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

        reasoning = await ReasoningService.build(
            db=db,
            repository_id=repository_id,
            query=search_query,
            top_k=10,
        )

        yield {
            "type": "reasoning",
            "data": reasoning,
        }

        # Build repository context

        context = ReasoningFormatter.format(
            reasoning
        )

        # Build final prompt

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + PromptBuilder.build(
                history=history,
                context=context,
                question=question,
            )
        )

        print("=" * 80)
        print("PROMPT SIZE:", len(prompt))
        print("=" * 80)

        response = model.generate_content(
            prompt,
            stream=True,
        )

        for chunk in response:
            if chunk.text:
                yield {
                    "type": "token",
                    "data": chunk.text,
                }