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

        print("\n" + "=" * 80)
        print("GRAPH SERVICE STARTED")
        print("=" * 80)

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
        print("SYMBOL TYPES")
        print("=" * 80)

        print("=" * 80)
        print("ALL SYMBOL TYPES")
        print("=" * 80)

        for s in symbols:
            print(s.symbol_name, " -> ", s.symbol_type)

        types = {}

        for s in symbols:
            types[s.symbol_type] = types.get(s.symbol_type, 0) + 1

        for k, v in types.items():
            print(k, ":", v)

        print("=" * 80)

        print("=" * 80)
        print("SYMBOLS FOUND:", len(symbols))
        print("=" * 80)

        edges = GraphBuilder.build(
            repository_id,
            symbols,
        )

        print("=" * 80)
        print("TOTAL EDGES:", len(edges))

        for edge in edges[:20]:
            print(
                edge.source_symbol,
                edge.relation,
                edge.target_symbol
            )

        print("=" * 80)

        for edge in edges:

            await GraphRepository.save(
                db,
                edge,
            )

        return {
            "symbols": len(symbols),
            "edges": len(edges),
        }