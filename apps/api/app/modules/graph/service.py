from sqlalchemy import select

from app.modules.graph.builder import GraphBuilder
from app.modules.graph.repository import GraphRepository
from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile


class GraphService:

    @staticmethod
    async def build_graph(
        db,
        repository_id,
    ):

        result = await db.execute(

            select(CodeSymbol)

            .join(

                RepositoryFile,

                RepositoryFile.id == CodeSymbol.repository_file_id,

            )

            .where(

                RepositoryFile.repository_id == repository_id

            )

        )

        symbols = result.scalars().all()

        print("=" * 80)
        print("SYMBOLS FOUND:", len(symbols))
        print("=" * 80)

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