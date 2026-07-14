from sqlalchemy import select, delete

from app.modules.repository_index.models import RepositoryFile
from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryIndexRepository:

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        items: list,
    ):

        db.add_all(items)

        await db.commit()

    @staticmethod
    async def get_files(
        db,
        repository_id,
    ):

        result = await db.execute(

            select(RepositoryFile)

            .where(
                RepositoryFile.repository_id == repository_id
            )

        )

        return result.scalars().all()

    @staticmethod
    async def delete_file(
        db,
        repository_file,
    ):

        await db.delete(repository_file)

        await db.commit()