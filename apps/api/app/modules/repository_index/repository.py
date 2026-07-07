from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.repository_index.models import RepositoryFile


class RepositoryIndexRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        files: list[RepositoryFile],
    ):
        db.add_all(files)
        await db.commit()