from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.embeddings.models import CodeEmbedding


class EmbeddingRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        items: list[CodeEmbedding],
    ):

        try:

            db.add_all(items)

            await db.commit()

            print(f"Inserted {len(items)} embeddings")

        except Exception as e:

            await db.rollback()

            print("=" * 80)
            print("INSERT ERROR")
            print(type(e))
            print(e)
            print("=" * 80)

            raise