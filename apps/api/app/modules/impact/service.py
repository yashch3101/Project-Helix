from app.modules.impact.repository import (
    ImpactRepository,
)


class ImpactService:

    @staticmethod
    async def analyze(
        db,
        repository_id,
        symbol,
    ):

        edges = await ImpactRepository.get_connections(
            db,
            repository_id,
            symbol,
        )

        callers = []
        callees = []

        for edge in edges:

            if edge.target_symbol == symbol:

                callers.append(edge.source_symbol)

            if edge.source_symbol == symbol:

                callees.append(edge.target_symbol)

        return {

            "symbol": symbol,

            "callers": callers,

            "callees": callees,

        }