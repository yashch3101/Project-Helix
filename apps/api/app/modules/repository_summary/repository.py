from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.repository_summary.models import RepositorySummary


class RepositorySummaryRepository:

    @staticmethod
    async def get(
        db: AsyncSession,
        repository_id: UUID,
    ):

        result = await db.execute(
            select(RepositorySummary).where(
                RepositorySummary.repository_id == repository_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def save_or_update(
        db: AsyncSession,
        summary: RepositorySummary,
    ):

        existing = await RepositorySummaryRepository.get(
            db,
            summary.repository_id,
        )

        if existing:

            existing.language = summary.language
            existing.framework = summary.framework
            existing.repository_type = summary.repository_type
            existing.entry_points = summary.entry_points
            existing.api_routes = summary.api_routes
            existing.total_files = summary.total_files
            existing.total_classes = summary.total_classes
            existing.total_functions = summary.total_functions
            existing.total_modules = summary.total_modules
            existing.important_modules = summary.important_modules
            existing.architecture = summary.architecture
            existing.execution_flow = summary.execution_flow
            existing.knowledge_card = summary.knowledge_card

            await db.commit()
            await db.refresh(existing)

            return existing

        db.add(summary)

        await db.commit()

        await db.refresh(summary)

        return summary

    @staticmethod
    async def update(
        db: AsyncSession,
        summary: RepositorySummary,
    ):

        await db.commit()

        await db.refresh(summary)

        return summary