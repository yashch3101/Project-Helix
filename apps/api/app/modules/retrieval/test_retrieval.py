import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.retrieval.service import RetrievalService


async def main():

    repository_id = input("Repository ID: ")

    query = input("Question: ")

    async with AsyncSessionLocal() as db:

        results = await RetrievalService.search(
            db=db,
            repository_id=repository_id,
            query=query,
            top_k=5,
        )

        print("\n" + "=" * 80)

        for i, item in enumerate(results, 1):

            chunk = item["chunk"]

            print(f"\nResult #{i}")
            print("-" * 80)
            print("Score :", round(item["score"], 4))
            print("Chunk :", chunk.chunk_name)
            print("Type  :", chunk.chunk_type)
            print("Lines :", f"{chunk.start_line}-{chunk.end_line}")
            print()
            print(chunk.content[:500])


if __name__ == "__main__":
    asyncio.run(main())