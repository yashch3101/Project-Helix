import google.generativeai as genai  # type: ignore[import]

from app.core.config import settings

genai.configure(
    api_key=settings.gemini_api_key,
)

model = genai.GenerativeModel(
    "gemini-2.5-flash",
)


class QueryRewriter:

    @staticmethod
    async def rewrite(
        history: str,
        question: str,
    ):

        if not history.strip():
            return question

        prompt = f"""
You are a query rewriting assistant.

Conversation:

{history}

Current Question:

{question}

Rewrite the current question into a standalone semantic search query.

Rules:

- Keep important technical names.
- Resolve "it", "this", "that".
- Do not answer.
- Return ONLY the rewritten query.
"""

        try:

            response = model.generate_content(
                prompt
            )

            rewritten = response.text.strip()

            if rewritten:
                return rewritten

        except Exception:
            pass

        return question