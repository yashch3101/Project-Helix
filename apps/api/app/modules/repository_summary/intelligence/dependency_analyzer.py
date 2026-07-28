from collections import defaultdict

from sqlalchemy import select

from app.modules.graph.models import GraphEdge


class DependencyAnalyzer:

    @staticmethod
    async def analyze(
        db,
        repository_id,
    ):

        result = await db.execute(

            select(GraphEdge).where(
                GraphEdge.repository_id == repository_id
            )
        )

        edges = result.scalars().all()

        dependencies = defaultdict(set)

        for edge in edges:

            source = edge.source_symbol

            target = edge.target_symbol

            if source and target:

                dependencies[source].add(target)

        return dependencies