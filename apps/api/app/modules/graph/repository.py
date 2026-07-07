from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.graph.models import GraphEdge


class GraphRepository:

    @staticmethod
    async def save(
        db: AsyncSession,
        edge: GraphEdge,
    ):
        db.add(edge)

        await db.commit()

        await db.refresh(edge)

        return edge