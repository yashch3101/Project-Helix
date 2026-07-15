import json

from app.modules.ai.groq_client import GroqClient

from app.modules.symbol_docs.models import (
    SymbolDocumentation,
)

from app.modules.symbol_docs.prompts import (
    SYSTEM_PROMPT,
)

from app.modules.symbol_docs.repository import (
    SymbolDocumentationRepository,
)


class SymbolDocumentationService:

    @staticmethod
    async def get_or_generate(
        db,
        symbol,
        source_code,
    ):

        print("=" * 80)
        print("STEP 1 : ENTERED DOC SERVICE")
        print(symbol.symbol_name)
        print("=" * 80)

        existing = await SymbolDocumentationRepository.get_by_symbol(
            db,
            symbol.id,
        )

        if existing:
            print("ALREADY EXISTS")
            return existing

        prompt = f"""
{SYSTEM_PROMPT}

Name:
{symbol.symbol_name}

Type:
{symbol.symbol_type}

Code:

{source_code}
"""

        print("STEP 2 : CALLING GEMINI")

        response = await GroqClient.generate(
            prompt,
            json_mode=True,
        )

        print("=" * 80)
        print("RAW RESPONSE")
        print(response)
        print("=" * 80)

        data = json.loads(response)

        print("=" * 80)
        print("DATA RECEIVED:")
        print(data)
        print(type(data))
        print("=" * 80)

        print("STEP 4 : JSON PARSED")

        doc = SymbolDocumentation(
            symbol_id=symbol.id,

            summary=data.get(
                "summary",
                data.get("description", "")
            ),

            explanation=data.get(
                "explanation",
                data.get("description", "")
            ),

            parameters=json.dumps(
                data.get("parameters", {}),
                indent=2,
            ),

            returns=str(
                data.get("returns", "")
            ),

            examples=json.dumps(
                data.get("examples", []),
                indent=2,
            ),
        )

        print("STEP 5 : SAVING")

        doc = await SymbolDocumentationRepository.create(
            db,
            doc,
        )

        print("STEP 6 : SAVED")

        return doc