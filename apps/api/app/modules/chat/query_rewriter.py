from app.modules.ai.groq_client import GroqClient


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

            response = await GroqClient.generate(prompt)

            rewritten = response.strip()

            if rewritten:
                return rewritten

        except Exception:
            pass

        return question