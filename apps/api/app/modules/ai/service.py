from app.modules.ai.groq_client import GroqClient

# from app.modules.ai.prompt import SYSTEM_PROMPT
from app.modules.reasoning.service import ReasoningService
from app.modules.ai.reasoning_formatter import ReasoningFormatter
from app.modules.ai.reasoning_prompt import SYSTEM_PROMPT
from app.modules.ai.prompt_builder import PromptBuilder


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

        response = await GroqClient.generate(prompt)

        yield {
            "type": "token",
            "data": response,
        }