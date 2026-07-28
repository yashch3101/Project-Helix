from app.modules.retrieval.service import RetrievalService

from .base import BaseTool
from .models import ToolResult


class VectorSearchTool(BaseTool):

    name = "vector_search"

    async def execute(
        self,
        db,
        repository_id,
        query: str,
        plan=None,
    ) -> ToolResult:

        try:

            results = await RetrievalService.search(
                db=db,
                repository_id=repository_id,
                query=query,
                top_k=plan.retrieval_limit,
            )

            return ToolResult(
                tool=self.name,
                success=True,
                data=results,
            )

        except Exception as e:

            return ToolResult(
                tool=self.name,
                success=False,
                error=str(e),
            )