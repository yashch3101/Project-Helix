import google.generativeai as genai # type: ignore[import]

from app.core.config import settings


genai.configure(
    api_key=settings.gemini_api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


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

        response = model.generate_content(
            prompt
        )

        return response.text.strip()