from sqlalchemy import select

from app.modules.parser.models import CodeSymbol

from app.modules.knowledge_graph.models import (
    SymbolRelationship,
)

from app.modules.knowledge_graph.repository import (
    KnowledgeGraphRepository,
)


class KnowledgeGraphService:

    @staticmethod
    async def build(
        db,
    ):

        print("=" * 80)
        print("BUILDING KNOWLEDGE GRAPH")
        print("=" * 80)

        symbols = (
            await db.execute(
                select(CodeSymbol)
            )
        ).scalars().all()

        symbol_map = {}

        for symbol in symbols:
            symbol_map[symbol.symbol_name] = symbol

        print(f"Loaded {len(symbols)} symbols")

        for symbol in symbols:

            if symbol.symbol_type != "import":
                continue

            imported_name = symbol.symbol_name.split(".")[-1]

            if imported_name not in symbol_map:
                continue

            target = symbol_map[imported_name]

            relationship = SymbolRelationship(

                from_symbol_id=symbol.id,

                to_symbol_id=target.id,

                relationship="IMPORTS",
            )

            await KnowledgeGraphRepository.create(
                db,
                relationship,
            )

            print(
                f"IMPORT : {symbol.symbol_name} ---> {target.symbol_name}"
            )

        print("=" * 80)
        print("KNOWLEDGE GRAPH COMPLETED")
        print("=" * 80)

        return True