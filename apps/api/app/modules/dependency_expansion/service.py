from app.modules.dependency_expansion.repository import (
    DependencyExpansionRepository,
)


class DependencyExpansionService:

    @staticmethod
    async def expand(
        db,
        repository_id,
        retrieval_results,
    ):

        expanded = []

        visited = set()

        for chunk in retrieval_results:

            if isinstance(chunk, dict):
                dependency_name = chunk.get("chunk_name")
            else:
                dependency_name = chunk.chunk_name

            if not dependency_name:
                continue

            dependencies = await (
                DependencyExpansionRepository.get_dependencies(
                    db=db,
                    repository_id=repository_id,
                    symbol_name=dependency_name,
                )
            )

            for dependency in dependencies:

                if dependency.id not in visited:

                    expanded.append(dependency)

                    visited.add(dependency.id)

        return expanded