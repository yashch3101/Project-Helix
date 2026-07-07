from sqlalchemy import select

from app.modules.graph.builder import GraphBuilder
from app.modules.graph.repository import GraphRepository
from app.modules.parser.models import CodeSymbol


class GraphService:

    @staticmethod
    async def build_graph(
        db,
        repository_id,
    ):

        result = await db.execute(
            select(CodeSymbol).where(
                CodeSymbol.repository_id == repository_id
            )
        )

        symbols = result.scalars().all()

        edges = GraphBuilder.build(
            repository_id,
            symbols,
        )

        for edge in edges:

            await GraphRepository.save(
                db,
                edge,
            )

        return {
            "symbols": len(symbols),
            "edges": len(edges),
        }