import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.dependency_graph.service import DependencyService

REPOSITORY_ID = "f3b6a70c-a21e-42ee-99ad-ac99d4493789"


async def main():

    async with AsyncSessionLocal() as db:

        result = await DependencyService.build(
            db,
            REPOSITORY_ID,
        )

        print("=" * 80)
        print(result)
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())