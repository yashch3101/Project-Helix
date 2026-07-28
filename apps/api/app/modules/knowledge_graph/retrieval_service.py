from sqlalchemy import select

from app.modules.parser.models import CodeSymbol

from app.modules.knowledge_graph.repository import (
    KnowledgeGraphRepository,
)


class GraphRetrievalService:

    @staticmethod
    async def expand(
        db,
        symbol_name,
    ):

        print("=" * 80)
        print("GRAPH EXPANSION")
        print(symbol_name)
        print("=" * 80)

        result = await db.execute(

            select(CodeSymbol).where(

                CodeSymbol.symbol_name == symbol_name

            )

        )

        symbol = result.scalar_one_or_none()

        if symbol is None:

            print("Symbol Not Found")

            return []

        print("Found Symbol")

        print(symbol.symbol_name)

        neighbors = await KnowledgeGraphRepository.get_neighbors(
            db,
            symbol.id,
        )

        print("=" * 80)
        print("NEIGHBORS FOUND:", len(neighbors))
        print("=" * 80)

        for edge in neighbors:

            print(
                edge.relationship,
                edge.from_symbol_id,
                edge.to_symbol_id,
            )

        return neighbors