from app.modules.graph_retrieval.repository import (
    GraphRetrievalRepository,
)


class GraphRetrievalService:

    @staticmethod
    async def expand(
        db,
        repository_id,
        symbols,
    ):

        visited = set()

        related = []

        for symbol in symbols:

            edges = await GraphRetrievalRepository.get_related_symbols(

                db=db,

                repository_id=repository_id,

                symbol_name=symbol,
            )

            for edge in edges:

                key = (
                    edge.source_symbol,
                    edge.target_symbol,
                    edge.relation,
                )

                if key in visited:
                    continue

                visited.add(key)

                related.append(edge)

        return related