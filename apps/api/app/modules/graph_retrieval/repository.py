from sqlalchemy import or_, select

from app.modules.graph.models import GraphEdge


class GraphRetrievalRepository:

    @staticmethod
    async def get_related_symbols(
        db,
        repository_id,
        symbol_name,
    ):

        result = await db.execute(

            select(GraphEdge)

            .where(
                GraphEdge.repository_id == repository_id
            )

            .where(

                or_(

                    GraphEdge.source_symbol == symbol_name,

                    GraphEdge.target_symbol == symbol_name,
                )
            )
        )

        return result.scalars().all()