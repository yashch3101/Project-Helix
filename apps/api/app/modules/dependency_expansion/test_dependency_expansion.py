import asyncio
from uuid import UUID

from app.db.session import AsyncSessionLocal

from app.modules.retrieval.service import RetrievalService
from app.modules.dependency_expansion.service import (
    DependencyExpansionService,
)

REPOSITORY_ID = UUID(
    "f3b6a70c-a21e-42ee-99ad-ac99d4493789"
)


async def main():

    async with AsyncSessionLocal() as db:

        retrieval = await RetrievalService.search(
            db=db,
            repository_id=REPOSITORY_ID,
            query="How does chat work?",
            top_k=5,
        )

        print("=" * 80)
        print("RETRIEVAL RESULTS:", len(retrieval))
        print("=" * 80)

        expanded = await DependencyExpansionService.expand(
            db=db,
            repository_id=REPOSITORY_ID,
            retrieval_results=retrieval,
        )

        print("=" * 80)
        print("AFTER DEPENDENCY EXPANSION:", len(expanded))
        print("=" * 80)

        for chunk in expanded[:20]:

            if isinstance(chunk, dict):

                print(
                    chunk["chunk_name"],
                    chunk["chunk_type"],
                )

            else:

                print(
                    chunk.chunk_name,
                    chunk.chunk_type,
                )


if __name__ == "__main__":
    asyncio.run(main())