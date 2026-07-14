import asyncio
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.modules.graph_retrieval.service import (
    GraphRetrievalService,
)

REPOSITORY_ID = UUID(
    "f3b6a70c-a21e-42ee-99ad-ac99d4493789"
)


async def main():

    async with AsyncSessionLocal() as db:

        result = await GraphRetrievalService.expand(

            db=db,

            repository_id=REPOSITORY_ID,

            symbols=[
                "fastapi.FastAPI",
            ],

        )

        print("=" * 80)

        print("EDGES:", len(result))

        for edge in result[:20]:

            print(
                edge.source_symbol,
                edge.relation,
                edge.target_symbol,
            )

        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())