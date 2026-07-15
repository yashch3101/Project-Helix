import json

from groq import AsyncGroq

from app.core.config import settings


class GroqClient:

    client = AsyncGroq(
        api_key=settings.groq_api_key,
    )

    MODEL = "llama-3.1-8b-instant"

    @staticmethod
    async def generate(
        prompt: str,
        json_mode: bool = False,
    ):

        kwargs = {
            "model": GroqClient.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0,
        }

        # Force JSON output whenever required
        if json_mode:
            kwargs["response_format"] = {
                "type": "json_object"
            }

        response = await GroqClient.client.chat.completions.create(
            **kwargs
        )

        content = response.choices[0].message.content

        if content is None:
            raise Exception("Groq returned an empty response.")

        return content.strip()