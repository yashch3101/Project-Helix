import asyncio

from app.db.session import AsyncSessionLocal
from app.modules.embeddings.service import EmbeddingService


async def main():

    async with AsyncSessionLocal() as db:

        total = await EmbeddingService.generate(db)

        print()

        print("=" * 50)
        print("Embeddings Generated:", total)
        print("=" * 50)


if __name__ == "__main__":

    asyncio.run(main())