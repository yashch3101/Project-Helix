from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dependency_graph.models import CodeDependency


class DependencyRepository:

    @staticmethod
    async def save(
        db: AsyncSession,
        dependency: CodeDependency,
    ):
        db.add(dependency)

    @staticmethod
    async def save_all(
        db: AsyncSession,
        dependencies: list[CodeDependency],
    ):
        db.add_all(dependencies)
        await db.commit()