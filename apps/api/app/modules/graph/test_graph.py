import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.graph.service import GraphService


REPOSITORY_ID = "f3b6a70c-a21e-42ee-99ad-ac99d4493789"


async def main():

    async with AsyncSessionLocal() as db:

        result = await GraphService.build_graph(
            db=db,
            repository_id=REPOSITORY_ID,
        )

        print()
        print("=" * 80)
        print(result)
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())