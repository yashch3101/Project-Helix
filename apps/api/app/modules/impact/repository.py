from sqlalchemy import or_, select

from app.modules.graph.models import GraphEdge


class ImpactRepository:

    @staticmethod
    async def get_connections(
        db,
        repository_id,
        symbol,
    ):
        result = await db.execute(

            select(GraphEdge)

            .where(
                GraphEdge.repository_id == repository_id
            )

            .where(
                or_(
                    GraphEdge.source_symbol == symbol,
                    GraphEdge.target_symbol == symbol,
                )
            )
        )

        return result.scalars().all()