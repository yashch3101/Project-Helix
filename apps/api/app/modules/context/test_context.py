import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.context.service import ContextService

REPOSITORY_ID = "f3b6a70c-a21e-42ee-99ad-ac99d4493789"


async def main():
    async with AsyncSessionLocal() as db:

        result = await ContextService.build(
            db=db,
            repository_id=REPOSITORY_ID,
            query="Explain the RAG pipeline",
            top_k=5,
        )

        print("=" * 80)
        print("TOTAL CONTEXT:", len(result))
        print("=" * 80)

        for item in result[:10]:
            print(item["chunk_name"])
            print(item["start_line"], "-", item["end_line"])
            print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())