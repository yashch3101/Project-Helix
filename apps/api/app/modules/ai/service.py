import re

from app.modules.ai.groq_client import GroqClient

# from app.modules.ai.prompt import SYSTEM_PROMPT
from app.modules.reasoning.service import ReasoningService
from app.modules.ai.reasoning_formatter import ReasoningFormatter
from app.modules.ai.reasoning_prompt import SYSTEM_PROMPT
from app.modules.ai.prompt_builder import PromptBuilder

import logging

logger = logging.getLogger(__name__)

MAX_PROMPT_CHARS = 14000
class AIService:

    @staticmethod
    async def build_reasoning(
        db,
        repository_id,
        search_query,
    ):
        return await ReasoningService.build(
            db=db,
            repository_id=repository_id,
            query=search_query,
        )

    @staticmethod
    def build_prompt(
        history,
        reasoning,
        question,
    ):
        context = ReasoningFormatter.format(reasoning)

        return (
            SYSTEM_PROMPT
            + "\n\n"
            + PromptBuilder.build(
                history=history,
                context=context,
                question=question,
            )
        )

    @staticmethod
    def is_small_talk(
        question: str,
    ) -> bool:

        text = re.sub(r"[^\w\s]", "", question.lower()).strip()

        small_talk = {
            "hi",
            "hello",
            "hey",
            "hii",
            "hiii",
            "hiiii",
            "heyy",
            "thanks",
            "thank you",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "who are you",
            "bye",
            "goodbye",
            "ok",
            "okay",
            "cool",
            "nice",
            "great",
            "yo",
            "sup",
        }

        return (
            text in small_talk
            or any(text.startswith(x + " ") for x in small_talk)
        )

    @staticmethod
    async def ask(
        db,
        repository_id,
        question: str,
        history: str = "",
        search_query: str = "",
    ):

        if AIService.is_small_talk(question):

            response = await GroqClient.generate(
                f"""
You are Project Helix, an AI software engineering assistant.

The user said:

"{question}"

Reply naturally in a friendly tone.

Keep the response under 2 sentences.

Do not analyze repositories, source code, or architecture unless the user explicitly asks.
"""
            )

            yield {
                "type": "token",
                "data": response,
            }

            return

        reasoning = await AIService.build_reasoning(
            db=db,
            repository_id=repository_id,
            search_query=search_query or question,
        )

        if not reasoning.get("retrieval"):

            yield {
                "type": "token",
                "data": "I couldn't find relevant information in this repository."
            }

            return

        yield {
            "type": "reasoning",
            "data": reasoning,
        }

        prompt = AIService.build_prompt(
            history=history,
            reasoning=reasoning,
            question=question,
        )

        if len(prompt) > MAX_PROMPT_CHARS:

            prompt = prompt[:MAX_PROMPT_CHARS]

            last_newline = prompt.rfind("\n")

            if last_newline > 0:
                prompt = prompt[:last_newline]

        try:

            response = await GroqClient.generate(
                prompt
            )

        except Exception:

            yield {
                "type": "token",
                "data": (
                    "Sorry, I couldn't generate a response right now. "
                    "Please try again."
                ),
            }

            return

        yield {
            "type": "token",
            "data": response,
        }