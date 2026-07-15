from app.modules.ai.groq_client import GroqClient


class TitleService:

    @staticmethod
    async def generate(
        question: str,
    ) -> str:

        prompt = f"""
Generate a very short chat title.

Rules:

- Maximum 5 words.
- Do not use quotes.
- Do not end with punctuation.
- Return ONLY the title.
- Make it descriptive.

User Message:

{question}
"""

        response = await GroqClient.generate(prompt)

        return response.strip()