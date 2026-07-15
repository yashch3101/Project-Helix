import asyncio
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.modules.reasoning.service import ReasoningService

REPOSITORY_ID = UUID(
    "f3b6a70c-a21e-42ee-99ad-ac99d4493789"
)


async def main():

    async with AsyncSessionLocal() as db:

        result = await ReasoningService.build(
            db=db,
            repository_id=REPOSITORY_ID,
            query="How does chat work?",
            top_k=10,
        )

        print("=" * 80)
        print("RETRIEVAL :", len(result["retrieval"]))
        print("=" * 80)

        print("GRAPH :", len(result["graph"]))
        print("=" * 80)

        print("DEPENDENCY :", len(result["dependency"]))
        print("=" * 80)

        print("CONTEXT :", len(result["context"]))
        print("=" * 80)

        print("=" * 80)

        print("TRACE")

        print(result["trace"])

        print("=" * 80)

        print("EVIDENCE")

        for item in result["evidence"]:

            print(item)

        print("=" * 80)

        print("=" * 80)

        print("IMPACT")

        for item in result["impact"][:20]:

            print(item)

        print("=" * 80)

        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())