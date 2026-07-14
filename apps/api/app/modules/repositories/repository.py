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

    @staticmethod
    async def get_by_project(
        db: AsyncSession,
        project_id,
    ):
        result = await db.execute(
            select(Repository)
            .where(
                Repository.project_id == project_id
            )
            .order_by(
                Repository.created_at.desc()
            )
        )

        return result.scalars().all()

    @staticmethod
    async def update_status(
        db: AsyncSession,
        repository: Repository,
        status: str,
    ):
        repository.status = status

        await db.commit()

        await db.refresh(repository)

        return repository

    @staticmethod
    async def update_local_path(
        db,
        repository,
        local_path: str,
    ):
        repository.local_path = local_path

        await db.commit()

        await db.refresh(repository)

        return repository