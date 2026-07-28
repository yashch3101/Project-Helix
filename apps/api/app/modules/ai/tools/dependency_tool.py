from .base import BaseTool
from .models import ToolResult


class DependencyTool(BaseTool):

    name = "dependency_search"

    async def execute(
        self,
        db,
        repository_id,
        query: str,
        plan=None,
    ) -> ToolResult:

        return ToolResult(
            tool=self.name,
            success=True,
            data={
                "query": query,
                "message": "Dependency search placeholder"
            },
        )