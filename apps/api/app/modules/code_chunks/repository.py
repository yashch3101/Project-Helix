from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.code_chunks.models import CodeChunk


class CodeChunkRepository:

    @staticmethod
    async def save_all(
        db: AsyncSession,
        chunks: list[CodeChunk],
    ):

        db.add_all(chunks)

        await db.commit()