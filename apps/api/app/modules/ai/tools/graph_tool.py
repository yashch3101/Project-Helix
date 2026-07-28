from app.modules.graph_retrieval.service import GraphRetrievalService

from .base import BaseTool
from .models import ToolResult


class GraphSearchTool(BaseTool):

    name = "graph_search"

    async def execute(
        self,
        db,
        repository_id,
        query,
        plan=None,
    ):

        try:

            # Intent analyzer ne entity detect ki thi.
            # Example:
            # Explain build_rag
            # entity -> build_rag

            symbols = []

            if getattr(plan, "entity", None):
                symbols.append(plan.entity)

            if not symbols:
                return ToolResult(
                    tool=self.name,
                    success=True,
                    data=[],
                )

            results = await GraphRetrievalService.expand(
                db=db,
                repository_id=repository_id,
                symbols=symbols,
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