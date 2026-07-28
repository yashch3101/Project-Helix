from dataclasses import dataclass, field

from app.modules.ai.tools.models import ToolResult


@dataclass
class RepositoryContext:

    vector_results: list = field(default_factory=list)

    graph_results: list = field(default_factory=list)

    dependency_results: list = field(default_factory=list)


class RepositoryContextBuilder:

    @staticmethod
    def build(
        tool_results: list[ToolResult],
    ) -> RepositoryContext:

        context = RepositoryContext()

        for result in tool_results:

            if not result.success:
                continue

            if result.tool == "vector_search":
                context.vector_results = result.data

            elif result.tool == "graph_search":
                context.graph_results = result.data

            elif result.tool == "dependency_search":
                context.dependency_results = result.data

        return context