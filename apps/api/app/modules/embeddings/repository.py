from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.embeddings.models import CodeEmbedding


class EmbeddingRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        items: list[CodeEmbedding],
    ):

        db.add_all(items)

        await db.commit()