from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.repositories.models import Repository


class RepositoryRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        repository: Repository,
    ):
        db.add(repository)
        await db.commit()
        await db.refresh(repository)
        return repository

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        repository_id,
    ):
        result = await db.execute(
            select(Repository).where(
                Repository.id == repository_id
            )
        )

        return result.scalar_one_or_none()